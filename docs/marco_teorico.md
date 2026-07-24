# Marco teórico

## TFIM

El modelo de Ising con campo transverso en 1D se escribe como

$$
H=-J\sum_i Z_iZ_{i+1}-h\sum_i X_i.
$$

El término $ZZ$ favorece orden ferromagnético en la dirección $Z$; el campo transversal $h$ introduce fluctuaciones cuánticas que polarizan el sistema en $X$. En el límite termodinámico, ambas tendencias compiten en $h/J=1$, donde aparece una transición de fase cuántica.

En cadenas finitas la transición no es una singularidad: se observa como un cruce suave en magnetización, correlaciones y brecha energética.

## Trotterización

Si el Hamiltoniano se separa en términos que no conmutan,

$$
H=H_{ZZ}+H_X,
$$

la evolución exacta se aproxima con pasos pequeños:

$$
e^{-iHt}\approx
\left(e^{-iH_{ZZ}\Delta t}e^{-iH_X\Delta t}\right)^r,
\qquad
\Delta t=t/r.
$$

El error disminuye al reducir $\Delta t$, lo que se verifica comparando fidelidad y observables contra diagonalización exacta.

## Diagonalización exacta

La ED construye la matriz completa del Hamiltoniano y obtiene eigenvalores/eigenvectores. Es una línea base clásica fuerte para sistemas pequeños, pero su memoria crece exponencialmente como $2^N$.

## VQE

El VQE prepara un estado variacional $|\psi(\theta)\rangle$ y minimiza

$$
E(\theta)=\langle\psi(\theta)|H|\psi(\theta)\rangle.
$$

En estos notebooks se usa un ansatz con rotaciones locales $R_XR_YR_Z$ y anillos de CNOT. El optimizador clásico es Adam.

## Fermi-Hubbard

El modelo de Fermi-Hubbard describe fermiones que saltan entre sitios y pagan una energía $U$ al ocupar doblemente un sitio:

$$
H=-t\sum_{\langle i,j\rangle,\sigma}
(c^\dagger_{i\sigma}c_{j\sigma}+h.c.)
+U\sum_i n_{i\uparrow}n_{i\downarrow}.
$$

Al crecer $U/t$, la doble ocupación se suprime y aparece el régimen de Mott. En el notebook opcional esto se observa mediante la doble ocupación y el observable $S(\pi)$.

## Referencias

1. S. Sachdev, *Quantum Phase Transitions*, 2nd ed., Cambridge University Press, 2011.
2. M. Suzuki, "Generalized Trotter's formula and systematic approximants of exponential operators and inner derivations with applications to many-body problems", *Communications in Mathematical Physics* **51**, 183-190, 1976.
3. S. Ebadi et al., "Quantum phases of matter on a 256-atom programmable quantum simulator", *Nature* **595**, 227-232, 2021.
4. J. Hubbard, "Electron correlations in narrow energy bands", *Proceedings of the Royal Society A* **276**, 238-257, 1963.
5. P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot", *Zeitschrift für Physik* **47**, 631-651, 1928.
6. A. Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor", *Nature Communications* **5**, 4213, 2014.
7. Track 3 del Quantathon CR 2026, `Track3.pdf`.

## Referencias de herramientas matemáticas

1. M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press, 2010. Formalismo de qubits, operadores de Pauli, circuitos y mediciones.
2. R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2013. Matrices hermitianas, espectros y fundamentos de diagonalización.
3. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra*, SIAM, 1997. Herramientas numéricas para resolver problemas espectrales.
4. G. H. Golub and C. F. Van Loan, *Matrix Computations*, Johns Hopkins University Press, 2013. Algoritmos matriciales usados para la línea base clásica.
5. N. J. Higham, *Functions of Matrices: Theory and Computation*, SIAM, 2008. Exponenciales de matrices y evolución temporal.
6. R. Courant and D. Hilbert, *Methods of Mathematical Physics, Vol. 1*, Wiley, 1989. Principio variacional/Rayleigh-Ritz.
7. H. F. Trotter, "On the product of semi-groups of operators", *Proceedings of the American Mathematical Society* **10**, 545-551, 1959. Fórmula producto de Trotter.
