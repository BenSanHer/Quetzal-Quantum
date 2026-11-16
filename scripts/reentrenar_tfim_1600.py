"""Repite seis VQE del TFIM con 1600 pasos y compara con el barrido de 800.

Desde la raíz del repositorio:
    python scripts/reentrenar_tfim_1600.py --workers 3

Se mantienen semillas, inicialización, ansatz, Adam, tolerancia y penalización.
Los entrenamientos independientes se pueden ejecutar en paralelo.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import sys
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FIELDS = (1.6, 1.8, 2.0)
SEEDS = (3, 42)
MAX_STEPS = 1600
TOL = 1e-9
PATIENCE = 25
OUTPUT = ROOT / "reports" / "tfim_vqe_1600"


def entrenar(h: float, seed: int) -> dict:
    import numpy as np
    import pennylane as qml

    from src.tfim.funciones_ising_hackathon import estado_base_exacto, vqe_ising

    start = perf_counter()
    print(f"Iniciando h/J={h:.1f}, semilla={seed}, máximo={MAX_STEPS}", flush=True)
    result = vqe_ising(
        n_qubits=6, J=1.0, h=h, n_layers=3,
        learning_rate=0.03, max_steps=MAX_STEPS,
        tol=TOL, patience=PATIENCE, seed=seed,
        calcular_exacto=False, verbose=False,
        paridad_objetivo=1, peso_paridad=1.0,
    )
    exact_energy, exact_state = estado_base_exacto(result["hamiltoniano"], 6)
    state = np.asarray(result["estado_vqe"])
    loss = np.asarray(result["historial_costo"])
    differences = np.abs(np.diff(loss))
    converged = len(differences) >= PATIENCE and bool(
        np.all(differences[-PATIENCE:] < TOL)
    )
    gradient = np.asarray(qml.grad(result["circuito_costo"])(result["parametros_optimos"]))
    row = {
        "h/J": h,
        "semilla": seed,
        "pasos": result["pasos_realizados"],
        "E_VQE": result["energia_vqe"],
        "E_exacta": exact_energy,
        "error_E": abs(result["energia_vqe"] - exact_energy),
        "costo": result["costo_vqe"],
        "paridad_VQE": result["paridad_vqe"],
        "fidelidad": float(abs(np.vdot(exact_state, state)) ** 2),
        "convergio": converged,
        "norma_gradiente": float(np.linalg.norm(gradient)),
        "rango_costo_ultimos_100": float(np.ptp(loss[-101:])),
        "cambio_costo_ultimos_100": float(loss[-1] - loss[-101]),
        "max_delta_costo_ultimos_25": float(np.max(differences[-PATIENCE:])),
        "costo_minimo_historial": float(np.min(loss)),
        "costo_paso_800": float(loss[800]),
        "energia_paso_800": float(result["historial"][800]),
        "paridad_paso_800": float(result["historial_paridad"][800]),
        "tiempo_s": perf_counter() - start,
    }
    OUTPUT.mkdir(exist_ok=True)
    np.savez_compressed(
        OUTPUT / f"h_{h:.1f}_semilla_{seed}.npz",
        h=h, J=1.0, n_qubits=6, n_layers=3, seed=seed,
        learning_rate=0.03, max_steps=MAX_STEPS, tol=TOL, patience=PATIENCE,
        paridad_objetivo=1, peso_paridad=1.0,
        estado_vqe=state, estado_exacto=exact_state,
        parametros_optimos=np.asarray(result["parametros_optimos"]),
        historial=np.asarray(result["historial"]),
        historial_costo=loss,
        historial_paridad=np.asarray(result["historial_paridad"]),
        gradiente=gradient,
    )
    print(
        f"Finalizado h/J={h:.1f}, semilla={seed}: "
        f"F={row['fidelidad']:.9f}, <P>={row['paridad_VQE']:.9f}, "
        f"pasos={row['pasos']}, convergió={converged}",
        flush=True,
    )
    return row


def main() -> None:
    import numpy as np
    import pandas as pd

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers debe ser al menos 1")
    baseline = pd.read_csv(ROOT / "reports" / "tfim_vqe_paridad.csv")
    OUTPUT.mkdir(exist_ok=True)
    rows = []
    start = perf_counter()
    with ProcessPoolExecutor(max_workers=min(args.workers, 6)) as pool:
        futures = [pool.submit(entrenar, h, seed) for h in FIELDS for seed in SEEDS]
        for future in as_completed(futures):
            rows.append(future.result())
            pd.DataFrame(rows).sort_values(["h/J", "semilla"]).to_csv(
                OUTPUT / "resultados_por_semilla.csv", index=False,
            )

    table = pd.DataFrame(rows).sort_values(["h/J", "semilla"])
    selected = table.loc[table.groupby("h/J")["costo"].idxmin()].sort_values("h/J")
    comparisons = []
    previous_states = np.load(ROOT / "reports" / "tfim_vqe_paridad_estados.npz")
    for _, current in selected.iterrows():
        h = float(current["h/J"])
        previous = baseline.loc[np.isclose(baseline["h/J"], h)].iloc[0]
        old_seed = int(previous["semilla"])
        rerun = np.load(OUTPUT / f"h_{h:.1f}_semilla_{old_seed}.npz")
        # Con las mismas semillas y parámetros, los primeros 800 pasos deben coincidir.
        for key in ("historial", "historial_costo", "historial_paridad"):
            np.testing.assert_allclose(
                rerun[key][:801], previous_states[f"h_{h:.1f}_{key}"],
                atol=1e-10, rtol=0,
            )
        comparisons.append({
            "h/J": h,
            "semilla_800": old_seed,
            "semilla_1600": int(current["semilla"]),
            "fidelidad_800": previous["fidelidad"],
            "fidelidad_1600": current["fidelidad"],
            "paridad_800": previous["paridad_VQE"],
            "paridad_1600": current["paridad_VQE"],
            "error_E_800": previous["error_E"],
            "error_E_1600": current["error_E"],
            "costo_800": previous["costo"],
            "costo_1600": current["costo"],
            "pasos_1600": int(current["pasos"]),
            "convergio_1600": bool(current["convergio"]),
            "norma_gradiente_1600": current["norma_gradiente"],
            "rango_costo_ultimos_100": current["rango_costo_ultimos_100"],
            "cambio_costo_ultimos_100": current["cambio_costo_ultimos_100"],
            "max_delta_costo_ultimos_25": current["max_delta_costo_ultimos_25"],
        })
    comparison = pd.DataFrame(comparisons)
    comparison.to_csv(ROOT / "reports" / "tfim_vqe_convergencia_1600.csv", index=False)
    (OUTPUT / "configuracion.json").write_text(json.dumps({
        "campos": FIELDS, "semillas": SEEDS, "n_qubits": 6, "J": 1.0,
        "n_layers": 3, "learning_rate": 0.03, "max_steps": MAX_STEPS,
        "tol": TOL, "patience": PATIENCE, "peso_paridad": 1.0,
        "paridad_objetivo": 1, "inicializacion": "mismas semillas, desde el inicio",
        "primeros_800_pasos_verificados": True,
        "tiempo_total_s": perf_counter() - start,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nComparación entre los resultados seleccionados:", flush=True)
    print(comparison.to_string(index=False), flush=True)
    print(f"\nTiempo total: {perf_counter() - start:.1f} s", flush=True)


if __name__ == "__main__":
    main()
