"""Continúa de h/J=0.8 a 2.0 con revisiones cada 100 pasos de Adam.

Se detiene cada campo al superar 99 % de fidelidad, por estancamiento de
dos bloques consecutivos o al alcanzar 800 pasos. Después pasa al siguiente
campo con los últimos parámetros, incluso si la parada fue por estancamiento.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FIELDS = (1.0, 1.2, 1.4, 1.6, 1.8, 2.0)
BLOCK_SIZE = 100
MAX_STEPS = 800
TARGET = 0.99
TOL_FIDELITY = 1e-4
TOL_MEAN_COST = 1e-4  # J=1; unidades de energía total del Hamiltoniano.
STABLE_BLOCKS = 2
OUTPUT = ROOT / "reports" / "tfim_vqe_continuacion_adaptativa"


def decidir_parada(actual: dict, anterior: dict | None) -> str | None:
    """Añade diferencias entre bloques y devuelve la causa de parada."""
    actual["delta_fidelidad_abs"] = None
    actual["delta_costo_medio_abs"] = None
    actual["bloques_estables"] = 0
    if anterior is not None:
        actual["delta_fidelidad_abs"] = abs(actual["fidelidad"] - anterior["fidelidad"])
        actual["delta_costo_medio_abs"] = abs(actual["costo_medio"] - anterior["costo_medio"])
        if (actual["delta_fidelidad_abs"] < TOL_FIDELITY
                and actual["delta_costo_medio_abs"] < TOL_MEAN_COST):
            actual["bloques_estables"] = anterior["bloques_estables"] + 1
    if actual["fidelidad"] > TARGET:
        return "fidelidad_objetivo"
    if actual["bloques_estables"] >= STABLE_BLOCKS:
        return "estancamiento"
    if actual["paso"] >= MAX_STEPS:
        return "limite_pasos"
    return None


def main() -> None:
    import numpy as np
    import pandas as pd

    from src.tfim.funciones_ising_hackathon import medir_observables_tfim, vqe_ising

    start = perf_counter()
    OUTPUT.mkdir(exist_ok=True)
    anchor = np.load(ROOT / "reports" / "tfim_vqe_warm_start_08_estados.npz", allow_pickle=False)
    references = np.load(ROOT / "reports" / "tfim_vqe_paridad_estados.npz", allow_pickle=False)
    baseline = pd.read_csv(ROOT / "reports" / "tfim_vqe_paridad.csv")
    initial_parameters = anchor["parametros_optimos"].copy()
    initial_state = anchor["estado_vqe"].copy()
    previous_h = 0.8
    summaries, all_blocks = [], []

    for h in FIELDS:
        prior = baseline.loc[np.isclose(baseline["h/J"], h)].iloc[0]
        exact = references[f"h_{h:.1f}_estado_exacto"].copy()
        initial_fidelity = float(abs(np.vdot(exact, initial_state)) ** 2)
        blocks, block_states, block_parameters = [], [], []
        print(f"\nh/J={h:.1f}, inicio desde {previous_h:.1f}, F inicial={initial_fidelity:.9f}", flush=True)

        def revisar(datos):
            step = datos["paso"]
            state = np.asarray(datos["estado"])
            row = {
                "h/J": h, "h_origen": previous_h, "paso": step,
                "energia": datos["energia"], "costo": datos["costo"],
                "costo_medio": float(np.mean(datos["historial_costo"][step-BLOCK_SIZE+1:step+1])),
                "fidelidad": float(abs(np.vdot(exact, state)) ** 2),
                "paridad": datos["paridad"],
            }
            reason = decidir_parada(row, blocks[-1] if blocks else None)
            row["motivo"] = reason or "continuar"
            blocks.append(row)
            all_blocks.append(dict(row))
            block_states.append(state.copy())
            block_parameters.append(np.asarray(datos["parametros"]).copy())
            pd.DataFrame(all_blocks).to_csv(OUTPUT / "bloques.csv", index=False)
            np.savez_compressed(
                OUTPUT / f"h_{h:.1f}.npz",
                h=h, h_origen=previous_h, J=1.0, n_qubits=6, n_layers=3,
                learning_rate=0.03, tamano_bloque=BLOCK_SIZE, max_steps=MAX_STEPS,
                fidelidad_objetivo=TARGET, tolerancia_fidelidad=TOL_FIDELITY,
                tolerancia_costo_medio=TOL_MEAN_COST, bloques_estables_requeridos=STABLE_BLOCKS,
                paridad_objetivo=1, peso_paridad=1.0,
                parametros_iniciales=initial_parameters,
                estado_inicial=initial_state, estado_exacto=exact,
                parametros_optimos=np.asarray(datos["parametros"]), estado_vqe=state,
                historial=datos["historial"], historial_costo=datos["historial_costo"],
                historial_paridad=datos["historial_paridad"],
                pasos_bloque=np.array([b["paso"] for b in blocks]),
                estados_bloque=np.asarray(block_states), parametros_bloque=np.asarray(block_parameters),
                motivo_parada=reason or "continuar",
            )
            print(
                f"  Paso {step:3d}: F={row['fidelidad']:.9f}, <P>={row['paridad']:.9f}, "
                f"L media={row['costo_medio']:.9f}, bloques estables={row['bloques_estables']}, "
                f"{row['motivo']}", flush=True,
            )
            return reason

        result = vqe_ising(
            n_qubits=6, J=1.0, h=h, n_layers=3,
            learning_rate=0.03, max_steps=MAX_STEPS,
            parametros_iniciales=initial_parameters,
            calcular_exacto=False, verbose=False,
            paridad_objetivo=1, peso_paridad=1.0,
            tamano_bloque=BLOCK_SIZE, callback_bloque=revisar,
        )
        state = np.asarray(result["estado_vqe"])
        fidelity = float(abs(np.vdot(exact, state)) ** 2)
        obs = medir_observables_tfim(state, 6)
        exact_obs = medir_observables_tfim(exact, 6)
        summaries.append({
            "h/J": h, "h_origen": previous_h,
            "fidelidad_anterior": prior["fidelidad"], "fidelidad_inicial": initial_fidelity,
            "fidelidad": fidelity, "objetivo_cumplido": fidelity > TARGET,
            "pasos": result["pasos_realizados"], "bloques": len(blocks),
            "motivo_parada": result["motivo_parada"],
            "E_VQE": result["energia_vqe"], "E_exacta": prior["E_exacta"],
            "error_E": abs(result["energia_vqe"] - prior["E_exacta"]),
            "costo": result["costo_vqe"], "paridad": result["paridad_vqe"],
            "delta_fidelidad_ultimo_bloque": blocks[-1]["delta_fidelidad_abs"],
            "delta_costo_medio_ultimo_bloque": blocks[-1]["delta_costo_medio_abs"],
            "bloques_estables": blocks[-1]["bloques_estables"],
            "Mx": obs["Mx"], "Mx_ED": exact_obs["Mx"],
            "Mz2": obs["Mz2"], "Mz2_ED": exact_obs["Mz2"],
            "Czz": obs["Czz"], "Czz_ED": exact_obs["Czz"],
        })
        pd.DataFrame(summaries).to_csv(ROOT / "reports" / "tfim_vqe_continuacion_adaptativa.csv", index=False)
        # La transferencia al siguiente campo también se realiza tras estancarse.
        initial_parameters = np.asarray(result["parametros_optimos"]).copy()
        initial_state = state.copy()
        previous_h = h

    config = {
        "campos": FIELDS, "origen": "parámetros guardados de la prueba 0.6 a 0.8",
        "n_qubits": 6, "J": 1.0, "n_layers": 3, "learning_rate": 0.03,
        "tamano_bloque": BLOCK_SIZE, "max_steps_por_campo": MAX_STEPS,
        "fidelidad_objetivo": TARGET, "comparacion_fidelidad": "mayor estricto",
        "tolerancia_fidelidad": TOL_FIDELITY, "tolerancia_costo_medio": TOL_MEAN_COST,
        "bloques_estables_requeridos": STABLE_BLOCKS,
        "mismo_adam_entre_bloques": True, "nuevo_adam_entre_campos": True,
        "avanzar_tras_estancamiento": True, "tiempo_total_s": perf_counter() - start,
    }
    (OUTPUT / "configuracion.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nResumen:", flush=True)
    print(pd.DataFrame(summaries).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
