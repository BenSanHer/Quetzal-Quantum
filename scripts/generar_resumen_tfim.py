"""Consolida los resultados guardados del TFIM sin volver a entrenar."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def generar_resumen():
    baseline = pd.read_csv(ROOT / "reports/tfim_vqe_paridad.csv")
    warm = pd.read_csv(ROOT / "reports/tfim_vqe_warm_start_08.csv").iloc[-1]
    adaptive = pd.read_csv(ROOT / "reports/tfim_vqe_continuacion_adaptativa.csv")
    rows = []
    for _, previous in baseline.iterrows():
        h = float(previous["h/J"])
        row = {
            "h/J": h, "fidelidad_independiente": previous["fidelidad"],
            "fidelidad": previous["fidelidad"], "paridad": previous["paridad_VQE"],
            "energia": previous["E_VQE"], "energia_exacta": previous["E_exacta"],
            "error_E": previous["error_E"], "costo": previous["costo"],
            "pasos_resultado": int(previous["pasos"]),
            "inicializacion": f"semilla {int(previous['semilla'])}; dos reinicios",
            "estrategia": "reinicios independientes con penalización",
            "fuente_tabla": "reports/tfim_vqe_paridad.csv",
            "archivo_estado": "reports/tfim_vqe_paridad_estados.npz",
            "clave_estado": f"h_{h:.1f}_estado_vqe",
            "clave_parametros": f"h_{h:.1f}_parametros_optimos",
        }
        if abs(h - 0.8) < 1e-9:
            row.update(
                fidelidad=warm["fidelidad"], paridad=warm["paridad"],
                energia=warm["energia"], error_E=warm["error_E"], costo=warm["costo"],
                pasos_resultado=int(warm["pasos"]), inicializacion="parámetros de 0.6",
                estrategia="continuación puntual, 800 pasos",
                fuente_tabla="reports/tfim_vqe_warm_start_08.csv",
                archivo_estado="reports/tfim_vqe_warm_start_08_estados.npz",
                clave_estado="estado_vqe", clave_parametros="parametros_optimos",
            )
        elif h > 0.8:
            current = adaptive.loc[(adaptive["h/J"] - h).abs() < 1e-9].iloc[0]
            row.update(
                fidelidad=current["fidelidad"], paridad=current["paridad"],
                energia=current["E_VQE"], error_E=current["error_E"], costo=current["costo"],
                pasos_resultado=int(current["pasos"]),
                inicializacion=f"parámetros de {current['h_origen']:.1f}",
                estrategia="continuación adaptativa",
                fuente_tabla="reports/tfim_vqe_continuacion_adaptativa.csv",
                archivo_estado=f"reports/tfim_vqe_continuacion_adaptativa/h_{h:.1f}.npz",
                clave_estado="estado_vqe", clave_parametros="parametros_optimos",
            )
        rows.append(row)
    table = pd.DataFrame(rows)
    table.to_csv(ROOT / "reports/tfim_vqe_resultados_finales.csv", index=False)
    return table


if __name__ == "__main__":
    print(generar_resumen().to_string(index=False))
