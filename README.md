<p align="center">
  <img src="assets/quetzal_quantum_logo.jpeg" alt="Quetzal Quantum logo" width="420">
</p>

# Challenge 3: Simulación de materiales para dispositivos de energía de próxima generación

Repositorio preparado para el **Track 3 / Challenge 3 del Quantathon CR 2026**. El reto consiste en simular materiales cuánticos que podrían ser relevantes para energía del futuro, como superconductores, baterías y catalizadores.

El núcleo de la entrega es el **Modelo de Ising de Campo Transverso (TFIM)**. Como extensión opcional se incluye un sistema pequeño del **modelo de Fermi-Hubbard**, útil para discutir electrones fuertemente correlacionados y el régimen de Mott.

ODS: **7, 9, 12 y 13**. La conexión física es que una mejor simulación de materiales puede apoyar energía más limpia, almacenamiento más eficiente, infraestructura científica y menor huella de carbono.

## Integrantes

- Benjamín Sánchez Hernández
- Arantxa Camil Junco Flores
- Amado Alberto Cabrera Estrada
- Mariana Elizabeth Perez
- Natalia Amortegui Castaño

## Estructura del repositorio

```text
Track3_Simulacion_Materiales/
├─ README.md
├─ requirements.txt
├─ run_all.py
├─ notebooks/
│  ├─ 01_tfim_trotter_ed_vqe.ipynb
│  └─ 02_fermi_hubbard_opcional.ipynb
├─ src/
│  ├─ tfim/
│  │  └─ funciones_ising_hackathon.py
│  └─ fermi_hubbard/
│     └─ Funciones_F_h.py
├─ docs/
│  ├─ Track3.pdf
│  ├─ marco_teorico.md
│  ├─ track3_checklist.md
│  └─ toolkit_statement.md
├─ reports/
│  ├─ informe_tecnico_borrador.md
│  └─ presentacion_5min_outline.md
└─ figures/
   └─ README.md
```

Los notebooks se separaron de las funciones para que el código sea más reproducible: los notebooks contienen parámetros, ejecución, tablas, figuras e interpretación; `src/` contiene las rutinas usadas para obtener los resultados.

## Instalación

Desde esta carpeta:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

## Dry run

Para verificar qué se ejecutaría sin correr simulaciones:

```bash
python run_all.py --dry-run
```

La dry run no ejecuta notebooks, no corre VQE y no genera archivos nuevos. Solo reporta cuántas celdas de código tiene cada notebook y cuántas celdas VQE serán omitidas.

## Punto de entrada reproducible

Para ejecutar los notebooks y guardar copias ejecutadas:

```bash
python run_all.py
```

Por indicación del flujo de trabajo actual, `run_all.py` **omite las celdas VQE** etiquetadas como `skip-vqe`. Esto permite reproducir Trotter, diagonalización exacta, barridos no variacionales, tablas y gráficas sin lanzar optimizaciones VQE largas. El código VQE queda escrito en los notebooks fuente para ejecutarse manualmente en el interior del Notebook.

Las copias ejecutadas se guardan en:

```text
executed_notebooks/
```

## Planteamiento del problema

El Track 3 pide:

1. Implementar la evolución temporal trotterizada del TFIM en 1D.
2. Graficar $\langle Z\rangle$ y $\langle Z_iZ_j\rangle$ contra tiempo desde un estado producto inicial.
3. Barrer $h/J\in\{0.5,1.0,2.0\}$ a través de la transición de fase.
4. Comparar frente a diagonalización exacta para una cadena de 6 qubits.
5. Opcionalmente, usar VQE para estimar la energía del estado fundamental.

El notebook principal cubre esos puntos. El notebook de Fermi-Hubbard queda como extensión opcional.

## Modelo TFIM

El TFIM describe una red de espines con acoplamientos $ZZ$ entre vecinos y un campo magnético transverso:

$$
H=-J\sum_i Z_iZ_{i+1}-h\sum_i X_i.
$$

La interacción $J$ favorece alineación ferromagnética en $Z$, mientras que el campo $h$ introduce fluctuaciones cuánticas en $X$. En el límite termodinámico la transición de fase ocurre en:

$$
h/J=1.
$$

En cadenas finitas, como $N=6$, la transición se observa redondeada.

## Resultados TFIM

Resultados de referencia obtenidos en los notebooks fuente:

| Prueba | Resultado |
|:--|:--|
| Degradación Trotter | $F(r,2r)$ baja de `0.977711` para $N=4$ a `0.949215` para $N=12$. |
| Dinámica $h/J=0.5$ | Fidelidad mínima Trotter-ED `0.981615`. |
| Dinámica $h/J=1.0$ | Fidelidad mínima Trotter-ED `0.964284`. |
| Dinámica $h/J=2.0$ | Fidelidad mínima Trotter-ED `0.920426`. |
| ED $N=6$, $h/J=0.5$ | $E_0/N=-1.064116$, $\sqrt{\langle M_z^2\rangle}=0.969914$. |
| ED $N=6$, $h/J=1.0$ | $E_0/N=-1.287901$, $\sqrt{\langle M_z^2\rangle}=0.813220$. |
| ED $N=6$, $h/J=2.0$ | $E_0/N=-2.128232$, $\sqrt{\langle M_z^2\rangle}=0.554173$. |

El VQE del TFIM queda escrito como extensión opcional siguiendo el protocolo original: $N=4$, dos semillas por campo y selección del resultado de menor energía.

## Fermi-Hubbard opcional

El hamiltoniano de Fermi-Hubbard modela salto de fermiones y penalización por doble ocupación:

$$
H=-t\sum_{\langle i,j\rangle,\sigma}
(c^\dagger_{i\sigma}c_{j\sigma}+h.c.)
+U\sum_i n_{i\uparrow}n_{i\downarrow}.
$$

El notebook opcional estudia dinámica, diagonalización exacta, doble ocupación, densidad, $S(\pi)$ y VQE escrito para ejecución manual.

Resultados de referencia:

| Prueba | Resultado |
|:--|:--|
| Error Trotter | RMSE baja de `0.03881` con `r=2` a `0.00374` con `r=20`. |
| VQE Fermi-Hubbard | Fidelidad entre `0.999961` y `1.000000` en el barrido $U/J=0,\ldots,9$. |
| Régimen de Mott | La doble ocupación baja de `0.250000` a `0.021547` al aumentar $U/J$. |
| Orden antiferromagnético | $S(\pi)$ sube de `0.250000` a `0.478453`. |

## Limitaciones honestas

- No se afirma ventaja cuántica.
- La diagonalización exacta y métodos clásicos como redes tensoriales siguen siendo más fuertes para estos tamaños.
- Los resultados son de simulación ideal, sin ruido de hardware.
- El Fermi-Hubbard incluido es una extensión pequeña, no una red 4x4 completa.
- Los VQE están escritos, pero `run_all.py` no los ejecuta por defecto.
- La transición en $h/J=1$ está redondeada por tamaño finito.

## Entrega pendiente

- Convertir el borrador de informe técnico en PDF de máximo 8 páginas.
- Preparar la presentación de 5 minutos.
- Si se desea competir con stack Quantinuum estricto, migrar la ejecución final a Pytket y/o Guppy y correr en emulador H2.

## Referencias

1. S. Sachdev, *Quantum Phase Transitions*, 2nd ed., Cambridge University Press, 2011.
2. M. Suzuki, "Generalized Trotter's formula and systematic approximants of exponential operators and inner derivations with applications to many-body problems", *Communications in Mathematical Physics* **51**, 183-190, 1976.
3. S. Ebadi et al., "Quantum phases of matter on a 256-atom programmable quantum simulator", *Nature* **595**, 227-232, 2021.
4. J. Hubbard, "Electron correlations in narrow energy bands", *Proceedings of the Royal Society A* **276**, 238-257, 1963.
5. P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot", *Zeitschrift für Physik* **47**, 631-651, 1928.
6. V. Havlíček et al., "Supervised learning with quantum-enhanced feature spaces", *Nature* **567**, 209-212, 2019. Referencia general para circuitos variacionales y kernels cuánticos.
7. A. Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor", *Nature Communications* **5**, 4213, 2014.
8. Track 3 del Quantathon CR 2026, `docs/Track3.pdf`.

## Referencias de herramientas matemáticas

1. M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press, 2010. Operadores de Pauli, estados de qubits, circuitos y mediciones.
2. R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2013. Álgebra lineal espectral, matrices hermitianas y propiedades de eigenvalores.
3. L. N. Trefethen and D. Bau III, *Numerical Linear Algebra*, SIAM, 1997. Diagonalización numérica, estabilidad y métodos clásicos de referencia.
4. G. H. Golub and C. F. Van Loan, *Matrix Computations*, Johns Hopkins University Press, 2013. Cómputo matricial usado en ED y comparación clásica.
5. N. J. Higham, *Functions of Matrices: Theory and Computation*, SIAM, 2008. Exponenciales de matrices y evolución temporal exacta.
6. R. Courant and D. Hilbert, *Methods of Mathematical Physics, Vol. 1*, Wiley, 1989. Principio variacional/Rayleigh-Ritz detrás del VQE.
7. H. F. Trotter, "On the product of semi-groups of operators", *Proceedings of the American Mathematical Society* **10**, 545-551, 1959. Fórmula producto usada en la trotterización.
