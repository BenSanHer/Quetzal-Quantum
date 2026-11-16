"""Comprueba que las revisiones por bloques conservan la trayectoria de Adam."""
import unittest

import numpy as np

from src.tfim.funciones_ising_hackathon import vqe_ising


class BloquesTFIMTests(unittest.TestCase):
    def ejecutar(self, **extra):
        options = dict(
            n_qubits=2, J=1.0, h=0.8, n_layers=1,
            parametros_iniciales=np.random.default_rng(7).normal(0, 0.1, (2, 2, 3)),
            max_steps=6, tol=0.0, patience=100,
            calcular_exacto=False, verbose=False,
        )
        options.update(extra)
        return vqe_ising(**options)

    def test_mismo_adam_y_mismos_parametros_entre_bloques(self):
        observado = []

        def revisar(datos):
            observado.append(datos["paso"])
            self.assertAlmostEqual(np.linalg.norm(datos["estado"]), 1.0)
            return "objetivo" if datos["paso"] == 6 else None

        continuo = self.ejecutar()
        por_bloques = self.ejecutar(tamano_bloque=2, callback_bloque=revisar)
        self.assertEqual(observado, [2, 4, 6])
        for key in ("historial", "historial_costo", "historial_paridad", "parametros_optimos"):
            np.testing.assert_array_equal(continuo[key], por_bloques[key])
        self.assertEqual(por_bloques["motivo_parada"], "objetivo")

    def test_callback_sustituye_la_parada_estricta(self):
        observado = []

        def revisar(datos):
            observado.append(datos["paso"])
            return "estancamiento" if datos["paso"] == 4 else None

        resultado = self.ejecutar(
            tol=1e6, patience=1, tamano_bloque=2, callback_bloque=revisar,
        )
        self.assertEqual(observado, [2, 4])
        self.assertEqual(resultado["pasos_realizados"], 4)
        self.assertEqual(resultado["motivo_parada"], "estancamiento")

    def test_evaluacion_al_final_de_un_bloque_parcial(self):
        observado = []
        self.ejecutar(max_steps=5, tamano_bloque=2, callback_bloque=lambda d: observado.append(d["paso"]))
        self.assertEqual(observado, [2, 4, 5])

    def test_valida_configuracion(self):
        for block in (0, -1, 2.5):
            with self.assertRaises(ValueError):
                self.ejecutar(tamano_bloque=block)
        with self.assertRaises(TypeError):
            self.ejecutar(callback_bloque=3)


if __name__ == "__main__":
    unittest.main()
