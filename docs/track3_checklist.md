# Checklist Track 3

Basado en `docs/Track3.pdf`.

## Núcleo obligatorio

- [x] Hamiltoniano del TFIM documentado.
- [x] Evolución temporal trotterizada.
- [x] Tamaño de paso de Trotter documentado.
- [x] Barrido en $h/J \in \{0.5, 1.0, 2.0\}$.
- [x] Gráficas de $\langle Z\rangle$ y $\langle Z_iZ_j\rangle$ vs. tiempo.
- [x] Magnetización en $Z$ y $X$ a través de la transición.
- [x] Comparación contra ED para 6 qubits.
- [x] Análisis de error de Trotter.
- [x] Limitaciones honestas.

## Extensiones opcionales

- [x] VQE para estimar energía fundamental del TFIM.
- [x] Penalización de paridad y continuación variacional con objetivo de fidelidad superior al 99 %.
- [x] Resultados, estados y parámetros guardados con procedencia por campo.
- [x] Bitácora experimental del 15 de noviembre de 2026 como complemento del informe original.
- [x] Fermi-Hubbard pequeño con diagonalización exacta.
- [x] Trotterización de Fermi-Hubbard.
- [x] Observables de Fermi-Hubbard: doble ocupación, densidad y $S(\pi)$.
- [x] VQE de Fermi-Hubbard.
- [ ] Ejecución en emulador H2.
- [ ] Mitigación de ruido o QEC.

## Entrega

- [x] README.
- [x] requirements.txt.
- [x] Punto de entrada reproducible (`run_all.py`).
- [x] Notebooks separados.
- [x] Código modular en `src/`.
- [x] Marco teórico.
- [x] Informe técnico de la entrega original en PDF; actualización VQE en [la bitácora](../reports/bitacora_tfim_2026-11-15.md) y el informe Markdown.
- [ ] Presentación de 5 minutos.
- [ ] Declaración final de SDK menor o igual a 200 palabras.

