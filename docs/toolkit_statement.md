# Declaración de SDK y herramientas

Versión breve para adaptar al límite de 200 palabras de la entrega:

> Para la versión local reproducible usamos Qiskit para construir circuitos de Trotter y simular vectores de estado, SciPy/NumPy para la diagonalización exacta y PennyLane para los VQE. Esta combinación permitió validar rápidamente el Hamiltoniano, los observables y los errores frente a una línea base clásica. El stack solicitado por Quantinuum para ejecución en H2 es Pytket y/o Guppy; la migración a ese stack queda identificada como siguiente paso para hardware/emulador. Lo que funcionó mejor fue separar funciones reutilizables en `src/` y dejar los notebooks como punto de entrada educativo. Lo que faltó fue una corrida cuantitativa en H2 con análisis de ruido o mitigación.

