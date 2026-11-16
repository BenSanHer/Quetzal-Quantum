# Informe técnico - versión Markdown actualizada

Actualización del TFIM: **15 de noviembre de 2026**. Esta versión complementa el PDF de la entrega original; el registro de decisiones y experimentos está en [la bitácora fechada](bitacora_tfim_2026-11-15.md).

## 1. Planteamiento del problema

Se estudia la simulación cuántica de modelos de materiales relevantes para energía limpia: el TFIM como sistema de espines con transición de fase cuántica y Fermi-Hubbard como modelo prototipo de electrones fuertemente correlacionados.

## 2. Línea base clásica

La referencia clásica es la diagonalización exacta. Para TFIM se usa una cadena de 6 qubits; para Fermi-Hubbard se usa un sistema pequeño a semillenado. La ED proporciona energías, estados y observables para comparar Trotter y VQE.

## 3. Implementación cuántica

El TFIM se implementa con circuitos de Trotter de primer orden, separando los términos $ZZ$ y $X$. El VQE usa rotaciones locales $R_XR_YR_Z$ y anillos de CNOT. Para TFIM minimiza $\mathcal L_+=\langle H\rangle+\lambda(1-\langle P\rangle)/2$, con $P=X_0X_1X_2X_3X_4X_5$ y $\lambda=J=1$, para favorecer la paridad positiva. Fermi-Hubbard incluye dinámica trotterizada y un VQE con penalización de sector físico.

## 4. Resultados

TFIM:

- Trotter presenta degradación con el tamaño para un paso fijo. ED proporciona la referencia de dinámica y observables para seis espines.
- El VQE usa tres capas de rotaciones y CNOT, Adam con tasa 0.03 y penalización de paridad positiva con λ=J=1. La energía física se distingue de la pérdida penalizada.
- Benjamín Sánchez Hernández propuso transferir los parámetros del campo anterior al siguiente, aprovechando la similitud entre fundamentales vecinos y el cambio suave de la cadena finita. La prueba 0.6 → 0.8 mejoró la fidelidad de 0.655755 a 0.998505.
- El criterio práctico autorizado fue fidelidad superior al 99 %, con revisiones cada 100 pasos, máximo de 800 y parada adicional por estancamiento. Se concretó como dos cambios de bloque consecutivos menores que 1e-4 en fidelidad y en pérdida media.
- Los seis campos de 1.0 a 2.0 superaron el objetivo en 100 pasos cada uno. Se usaron 600 pasos, frente a 4800 si se hubieran impuesto 800 por campo para ese tramo. Ninguno necesitó la parada por estancamiento.

Resultados finales, con procedencia y pasos del entrenamiento seleccionado:

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

Los primeros tres puntos proceden de reinicios independientes; 0.8 procede de la prueba puntual; los seis restantes corresponden a la continuación adaptativa. El [CSV consolidado](tfim_vqe_resultados_finales.csv) identifica los archivos de estado y parámetros de cada fila.

La [bitácora](bitacora_tfim_2026-11-15.md) conserva la secuencia experimental, incluyendo el ensayo de 1600 pasos que no mejoró apreciablemente los reinicios independientes. El cumplimiento del objetivo de fidelidad no se identifica con una convergencia numérica estricta del optimizador.


Disponibilidad de datos: el repositorio publica los CSV y las figuras. Los NPZ con estados y parámetros se generan localmente mediante las celdas de entrenamiento del notebook; el CSV consolidado conserva sus rutas como procedencia.

Fermi-Hubbard:

- El error Trotter disminuye al aumentar el número de pasos.
- Al crecer $U/J$, baja la doble ocupación y aumenta $S(\pi)$, señal del régimen de Mott.
- El VQE reproduce la ED con fidelidad cercana a 1 en el sistema pequeño.

## 5. Limitaciones

La parada por fidelidad utiliza el fundamental exacto disponible en este benchmark de seis espines. No se demuestra ventaja cuántica. Los resultados son de simulación ideal. La ED y métodos clásicos especializados siguen siendo más fuertes para tamaños pequeños y medianos. La extensión Fermi-Hubbard no alcanza una red 4x4 completa. Falta ejecución en emulador H2 y análisis de ruido.

## 6. ODS

La conexión principal es ODS 7: materiales con mejores propiedades electrónicas podrían habilitar transmisión o almacenamiento más eficiente de energía. También conecta con ODS 9, 12 y 13 por infraestructura científica, diseño sostenible y reducción potencial de huella climática.

## 7. Referencias

1. S. Sachdev, *Quantum Phase Transitions*, 2nd ed., Cambridge University Press, 2011.
2. M. Suzuki, "Generalized Trotter's formula and systematic approximants of exponential operators and inner derivations with applications to many-body problems", *Communications in Mathematical Physics* **51**, 183-190, 1976.
3. S. Ebadi et al., "Quantum phases of matter on a 256-atom programmable quantum simulator", *Nature* **595**, 227-232, 2021.
4. J. Hubbard, "Electron correlations in narrow energy bands", *Proceedings of the Royal Society A* **276**, 238-257, 1963.
5. P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot", *Zeitschrift für Physik* **47**, 631-651, 1928.
6. A. Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor", *Nature Communications* **5**, 4213, 2014.
7. Track 3 del Quantathon CR 2026, `docs/Track3.pdf`.

## 8. Referencias de herramientas matemáticas

1. M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press, 2010.
2. R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2013.
3. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra*, SIAM, 1997.
4. G. H. Golub and C. F. Van Loan, *Matrix Computations*, Johns Hopkins University Press, 2013.
5. N. J. Higham, *Functions of Matrices: Theory and Computation*, SIAM, 2008.
6. R. Courant and D. Hilbert, *Methods of Mathematical Physics, Vol. 1*, Wiley, 1989.
7. H. F. Trotter, "On the product of semi-groups of operators", *Proceedings of the American Mathematical Society* **10**, 545-551, 1959.
