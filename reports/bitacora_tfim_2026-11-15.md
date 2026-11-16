# Bitácora experimental del TFIM y complemento del informe

**Fecha: 15 de noviembre de 2026 (America/Mexico_City).**

Esta actualización complementa el [informe de la entrega original](informe_tecnico_track_3.pdf). Registra los experimentos realizados sobre el TFIM de seis espines, la propuesta de continuación de Benjamín Sánchez Hernández y los resultados que sustentan su adopción.

Disponibilidad: se publican el código, los resultados CSV y las figuras. Los archivos NPZ de estados, parámetros, gradientes e historiales se generan y conservan localmente. Sus rutas en los CSV identifican esa procedencia local.

## Problema observado

El Hamiltoniano periódico es `H = −J Σ ZᵢZᵢ₊₁ − h Σ Xᵢ`, con J=1. En el barrido original, una energía cercana a la exacta no aseguraba un buen estado: sin penalización se guardaron fidelidades 0.499992 en h/J=0.2, 0.488458 en 1.0 y 0.915772 en 2.0.

Para h>0, el fundamental de esta cadena finita pertenece al sector de paridad positiva. El operador `P = X₀X₁X₂X₃X₄X₅` conmuta con H. El costo se modificó a `L(θ) = ⟨H⟩ + λ(1 − ⟨P⟩)/2`, con λ=1. La penalización es el peso del sector negativo multiplicado por λ; energía física y costo se reportan por separado.

## Configuración común

| Parámetro | Valor |
|:--|:--|
| Espines y frontera | 6, periódica |
| Campos h/J | 0.2, 0.4, …, 2.0 |
| Ansatz | Rotaciones RX/RY/RZ y 3 capas de anillos de CNOT |
| Optimizador | Adam, tasa 0.03 |
| Simulador | PennyLane default.qubit, sin shots |
| Referencia | Diagonalización exacta |
| Paridad objetivo y penalización | +1, λ=J=1 |

## 1. Penalización y reinicios independientes

Se ejecutaron dos semillas por campo, 3 y 42, con hasta 800 pasos. Se conservó la menor pérdida penalizada. La penalización dio fidelidades próximas a 1 para 0.2–0.6, pero dejó mezcla de paridades en 0.8–1.4. En 1.6–2.0 la paridad era casi positiva y la fidelidad seguía entre 0.86 y 0.92.

Datos: [tabla por campo](tfim_vqe_paridad.csv) y `tfim_vqe_paridad_estados.npz`.

## 2. Duplicación del número de pasos

Se repitieron las seis combinaciones de campo y semilla de 1.6, 1.8 y 2.0 con 1600 pasos, manteniendo la configuración. Los primeros 800 pasos de las semillas previamente seleccionadas coincidieron exactamente con los historiales anteriores. Las fidelidades seleccionadas cambiaron de 0.859696 a 0.859672, de 0.893267 a 0.893285 y de 0.915768 a 0.915765.

Ninguna corrida alcanzó el criterio estricto original de variación de pérdida menor que 1e-9 durante 25 pasos consecutivos. La observación permite afirmar que más pasos con esa configuración no mejoraron apreciablemente los estados; no demuestra convergencia al mínimo global.

Datos: [comparación 800/1600](tfim_vqe_convergencia_1600.csv), [todas las semillas](tfim_vqe_1600/resultados_por_semilla.csv) y los archivos NPZ en `tfim_vqe_1600/`.

## 3. Hipótesis propuesta por Benjamín y prueba controlada

Benjamín propuso que los fundamentales de campos cercanos debían parecerse y que el cambio suave de la cadena finita permitiría usar los parámetros optimizados de un campo como inicio del siguiente. La regla aplicada fue `θ_inicial(h_siguiente) = θ_final(h_anterior)`.

La cercanía se comprobó con las referencias exactas guardadas: la fidelidad entre fundamentales vecinos fue 0.982972 para 0.2 → 0.4, 0.958711 para 0.8 → 1.0 y 0.998036 para 1.8 → 2.0. El menor valor de toda la malla fue 0.958711. Esta comprobación motivó una prueba puntual antes de modificar el barrido completo.

Se entrenó únicamente 0.8 con los parámetros guardados de 0.6. Se transfirieron los ángulos del circuito y se creó un Adam nuevo; se conservaron el ansatz, costo, tasa y máximo de 800 pasos.

| Estado evaluado en h/J=0.8 | Fidelidad | Paridad | Error de energía |
|:--|---:|---:|---:|
| VQE independiente anterior | 0.655755 | 0.394367 | 0.193211 |
| Parámetros de 0.6 antes de entrenar | 0.958536 | 0.999992 | 0.102428 |
| Después de entrenar en 0.8 | 0.998505 | 0.999981 | 0.009777 |

El mismo ansatz encontró un estado mucho mejor al cambiar la inicialización. La pérdida todavía oscilaba; la mejora de fidelidad se distingue del cumplimiento del criterio estricto de parada.

Datos: [comparación puntual](tfim_vqe_warm_start_08.csv) y `tfim_vqe_warm_start_08_estados.npz`.

## 4. Criterio práctico y condición adicional del usuario

Benjamín estableció que bastaba una fidelidad superior al 99 % y autorizó revisar en bloques de 100 pasos. Añadió que, si el entrenamiento se estabilizaba en otro valor y las diferencias entre bloques eran demasiado pequeñas, debía detenerse y continuar con el siguiente campo.

La operacionalización implementada fue:

1. Revisar al terminar cada bloque de 100 pasos, con máximo de 800 por campo.
2. Detener si la fidelidad es estrictamente mayor que 0.99.
3. Detener por estancamiento si, durante dos comparaciones consecutivas, el cambio absoluto de fidelidad es menor que 1e-4 y el de la pérdida media del bloque es menor que 1e-4 J. Estos umbrales concretan la condición cualitativa de mejora insuficiente.
4. Conservar el estado interno de Adam entre bloques del mismo campo. Al cambiar de Hamiltoniano, crear un Adam nuevo y reutilizar los últimos parámetros del circuito.
5. Avanzar al siguiente campo también tras estancamiento o límite, indicando si no se alcanzó el objetivo.

La trayectoria comenzó con los nuevos parámetros de 0.8 y avanzó por 1.0, 1.2, 1.4, 1.6, 1.8 y 2.0. Los seis casos superaron 0.99 en el primer bloque de 100 pasos. Ninguno activó la parada por estancamiento ni por límite. Ese criterio adicional quedó implementado y cubierto por pruebas.

Se usaron **600 pasos para esos seis campos**. Un presupuesto fijo de 800 por campo habría requerido 4800: la reducción frente a ese presupuesto es 87.5 %. Esta comparación se refiere al tramo adaptativo y no al costo total de todos los ensayos exploratorios.

## 5. Resultados consolidados

| h/J | Fidelidad final | Paridad | Error absoluto de energía | Pasos del resultado | Inicio |
|---:|---:|---:|---:|---:|:--|
| 0.2 | 0.999788 | 0.999857 | 0.001008 | 800 | semilla 3; dos reinicios |
| 0.4 | 0.998895 | 0.999972 | 0.003997 | 800 | semilla 42; dos reinicios |
| 0.6 | 0.998948 | 0.999992 | 0.005217 | 800 | semilla 42; dos reinicios |
| 0.8 | 0.998505 | 0.999981 | 0.009777 | 800 | parámetros de 0.6 |
| 1.0 | 0.997967 | 0.999999 | 0.014043 | 100 | parámetros de 0.8 |
| 1.2 | 0.998219 | 0.999999 | 0.012284 | 100 | parámetros de 1.0 |
| 1.4 | 0.998818 | 1.000000 | 0.008603 | 100 | parámetros de 1.2 |
| 1.6 | 0.999274 | 1.000000 | 0.005686 | 100 | parámetros de 1.4 |
| 1.8 | 0.999561 | 1.000000 | 0.003768 | 100 | parámetros de 1.6 |
| 2.0 | 0.999728 | 1.000000 | 0.002562 | 100 | parámetros de 1.8 |

La tabla combina ejecuciones con procedencias explícitas; no corresponde a una nueva trayectoria completa iniciada en 0.2. Los campos 0.2–0.6 conservan los resultados de reinicios independientes, 0.8 corresponde a la prueba puntual y 1.0–2.0 a la continuación adaptativa.

Comparación de la inicialización independiente penalizada contra la solución final seleccionada:

| h/J | Reinicios con penalización | Resultado final |
|---:|---:|---:|
| 0.2 | 0.999788 | 0.999788 |
| 0.4 | 0.998895 | 0.998895 |
| 0.6 | 0.998948 | 0.998948 |
| 0.8 | 0.655755 | 0.998505 |
| 1.0 | 0.551053 | 0.997967 |
| 1.2 | 0.556062 | 0.998219 |
| 1.4 | 0.664466 | 0.998818 |
| 1.6 | 0.859696 | 0.999274 |
| 1.8 | 0.893267 | 0.999561 |
| 2.0 | 0.915768 | 0.999728 |

Los valores completos y las rutas a cada estado y conjunto de parámetros están en [tfim_vqe_resultados_finales.csv](tfim_vqe_resultados_finales.csv).

## 6. Interpretación y alcance

- La penalización de paridad y la inicialización resuelven aspectos distintos. La primera favorece el sector correcto; la continuación ayudó a encontrar una mejor solución dentro de la misma familia de circuitos.
- La duplicación de pasos por sí sola no mejoró el caso independiente; reutilizar parámetros cambió sustancialmente los resultados de este estudio.
- Todos los puntos finales superan 99 % de fidelidad. Esto no equivale a demostrar un mínimo global del ansatz ni una convergencia numérica estricta de Adam.
- La transición en seis espines es un cruce suave. Se guardan Mx, Mz² y Czz y sus referencias exactas para revisar el cambio de régimen.
- La fidelidad con ED se usa como evaluación y criterio de parada de este benchmark pequeño. La función de costo optimizada utiliza H y P. La disponibilidad del fundamental exacto forma parte del alcance de esta validación.
- Son simulaciones ideales sin ruido de hardware; estos ensayos no establecen ventaja cuántica.

## 7. Reproducción y comprobaciones

```bash
python scripts/reentrenar_tfim_1600.py --workers 3
python scripts/continuar_tfim_adaptativo.py
python scripts/generar_resumen_tfim.py
python -m unittest discover -s tests -v
```

La primera orden reproduce el ensayo exploratorio de 1600 pasos. La segunda reproduce la continuación desde el estado de 0.8 generado localmente. En un clon nuevo, ejecutar primero las celdas de importación y parámetros, la sección 5 y la prueba puntual de la sección 7 del notebook para generar los archivos NPZ de referencia. La prueba puntual 0.6 → 0.8 se reproduce desde su celda del notebook principal. La tercera orden consolida los datos guardados sin volver a entrenar.

Se comprobaron independientemente energías, fidelidades y paridades con matrices del Hamiltoniano; la transferencia exacta de parámetros y estados entre campos; y las causas de parada. Las 14 pruebas cubren el costo y su gradiente, la selección de reinicios, la continuidad de Adam entre bloques y los criterios de objetivo y estancamiento.

Figuras: [continuación adaptativa](../figures/tfim_vqe_continuacion_adaptativa.png), [prueba 0.6 → 0.8](../figures/tfim_vqe_warm_start_08.png) y [diagnóstico de 1600 pasos](../figures/tfim_vqe_1600_convergencia.png).

## Referencias conceptuales

- A. Garcia-Saez y J. I. Latorre, *Addressing hard classical problems with Adiabatically Assisted Variational Quantum Eigensolvers* (2018), [arXiv:1806.02287](https://arxiv.org/abs/1806.02287). Contexto de la continuación variacional.
- B. Damski y M. M. Rams, *Exact results for fidelity susceptibility of the quantum Ising model: The interplay between parity, system size, and magnetic field*, J. Phys. A 47, 025303 (2014), [arXiv:1308.5917](https://arxiv.org/abs/1308.5917). Paridad y fidelidad en cadenas finitas.
