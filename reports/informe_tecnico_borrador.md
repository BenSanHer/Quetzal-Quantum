# Informe técnico - borrador

## 1. Planteamiento del problema

Se estudia la simulación cuántica de modelos de materiales relevantes para energía limpia: el TFIM como sistema de espines con transición de fase cuántica y Fermi-Hubbard como modelo prototipo de electrones fuertemente correlacionados.

## 2. Línea base clásica

La referencia clásica es la diagonalización exacta. Para TFIM se usa una cadena de 6 qubits; para Fermi-Hubbard se usa un sistema pequeño a semillenado. La ED proporciona energías, estados y observables para comparar Trotter y VQE.

## 3. Implementación cuántica

El TFIM se implementa con circuitos de Trotter de primer orden, separando los términos $ZZ$ y $X$. El VQE usa rotaciones locales $R_XR_YR_Z$ y anillos de CNOT. Fermi-Hubbard incluye dinámica trotterizada y un VQE con penalización de sector físico.

## 4. Resultados

TFIM:

- La fidelidad Trotter-ED disminuye al crecer el número de espines con paso fijo.
- En $h/J=1$ se observa el cambio de régimen esperado, redondeado por tamaño finito.
- El VQE recuperado trabaja en $N=4$ con dos semillas por campo y fidelidades cercanas a 1.

Fermi-Hubbard:

- El error Trotter disminuye al aumentar el número de pasos.
- Al crecer $U/J$, baja la doble ocupación y aumenta $S(\pi)$, señal del régimen de Mott.
- El VQE reproduce la ED con fidelidad cercana a 1 en el sistema pequeño.

## 5. Limitaciones

No se demuestra ventaja cuántica. Los resultados son de simulación ideal. La ED y métodos clásicos especializados siguen siendo más fuertes para tamaños pequeños y medianos. La extensión Fermi-Hubbard no alcanza una red 4x4 completa. Falta ejecución en emulador H2 y análisis de ruido.

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
