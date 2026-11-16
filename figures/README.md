# Figuras del TFIM

Actualización: 15 de noviembre de 2026. Las figuras se generaron con los datos guardados en `reports/`; el notebook principal incluye las salidas correspondientes.

| Figura | Qué muestra |
|:--|:--|
| [Continuación adaptativa](tfim_vqe_continuacion_adaptativa.png) | Comparación con los reinicios independientes, paridad final y pasos por campo. Los seis casos nuevos superaron 99 % en 100 pasos cada uno. |
| [Prueba puntual 0.6 → 0.8](tfim_vqe_warm_start_08.png) | Error de energía, paridad y variación de pérdida al transferir los parámetros de 0.6. |
| [Pérdida hasta 1600 pasos](tfim_vqe_1600_perdida.png) | Ensayo exploratorio de las dos semillas en 1.6, 1.8 y 2.0 antes de usar continuación. |
| [Diagnóstico de 1600 pasos](tfim_vqe_1600_convergencia.png) | Oscilaciones de la pérdida frente al criterio estricto original; las fidelidades no mejoraron apreciablemente al duplicar pasos. |

La [bitácora experimental](../reports/bitacora_tfim_2026-11-15.md) identifica los datos, la configuración y la propuesta que motivó cada ensayo.

