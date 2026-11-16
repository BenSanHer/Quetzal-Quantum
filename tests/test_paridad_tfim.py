"""Comprueba el costo de paridad, su gradiente y la selección de reinicios."""

import unittest
from unittest.mock import patch

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

from src.tfim import funciones_ising_hackathon as tfim


class CostoParidadTFIMTests(unittest.TestCase):
    def ejecutar(self, parametros, objetivo=1, peso=2.3, pasos=0):
        return tfim.vqe_ising(
            n_qubits=2, J=1.0, h=0.7, n_layers=1,
            parametros_iniciales=parametros, max_steps=pasos,
            paridad_objetivo=objetivo, peso_paridad=peso,
            calcular_exacto=False, verbose=False,
        )

    def test_penalizacion_en_ambos_sectores_y_en_una_mezcla(self):
        for paridad in (-1, 1):
            parametros = np.zeros((2, 2, 3))
            parametros[0, 0, 1] = paridad * np.pi / 2
            for objetivo in (-1, 1):
                with self.subTest(paridad=paridad, objetivo=objetivo):
                    resultado = self.ejecutar(parametros, objetivo=objetivo)
                    self.assertAlmostEqual(resultado["paridad_vqe"], paridad)
                    self.assertAlmostEqual(resultado["energia_vqe"], -1.0)
                    penalizacion = 0.0 if paridad == objetivo else 2.3
                    self.assertAlmostEqual(
                        resultado["costo_vqe"], -1.0 + penalizacion
                    )
        mezcla = self.ejecutar(np.zeros((2, 2, 3)))
        self.assertAlmostEqual(mezcla["paridad_vqe"], 0.0)
        self.assertAlmostEqual(mezcla["penalizacion_paridad"], 2.3 / 2)

    def test_costo_y_gradiente_contra_operador_matricial(self):
        parametros = pnp.array(
            np.random.default_rng(7).normal(0, 0.4, (2, 2, 3)),
            requires_grad=True,
        )
        resultado = self.ejecutar(parametros, objetivo=-1)
        H = tfim.matriz_operador(resultado["hamiltoniano"], 2)
        X = np.array([[0.0, 1.0], [1.0, 0.0]])
        H_costo = H + 2.3 * (np.eye(4) + np.kron(X, X)) / 2

        def costo_matricial(valores):
            estado = np.asarray(resultado["circuito_estado"](valores))
            return float(np.vdot(estado, H_costo @ estado).real)

        self.assertAlmostEqual(resultado["costo_vqe"], costo_matricial(parametros))
        gradiente = qml.grad(resultado["circuito_costo"])(parametros)
        gradiente_fd = np.zeros_like(parametros)
        eps = 1e-6
        for indice in np.ndindex(parametros.shape):
            mas = np.array(parametros)
            menos = np.array(parametros)
            mas[indice] += eps
            menos[indice] -= eps
            gradiente_fd[indice] = (
                costo_matricial(mas) - costo_matricial(menos)
            ) / (2 * eps)
        np.testing.assert_allclose(gradiente, gradiente_fd, atol=1e-7, rtol=1e-5)

    def test_peso_cero_e_historial_del_optimizador(self):
        resultado = self.ejecutar(np.zeros((2, 2, 3)), peso=0.0, pasos=3)
        np.testing.assert_allclose(resultado["historial"], resultado["historial_costo"])
        self.assertEqual(len(resultado["historial_paridad"]), 4)
        self.assertAlmostEqual(
            resultado["energia_vqe"],
            float(resultado["circuito_energia"](resultado["parametros_optimos"])),
        )

    def test_reinicio_seleccionado_por_costo_y_no_solo_por_energia(self):
        menor_energia = {"energia_vqe": -2.0, "costo_vqe": -1.0}
        menor_costo = {"energia_vqe": -1.9, "costo_vqe": -1.8}
        with patch.object(tfim, "vqe_ising", side_effect=[menor_energia, menor_costo]) as ejecutar:
            mejor = tfim.mejor_vqe_ising(
                n_qubits=2, J=1.0, h=0.7, seeds=(3, 42),
                paridad_objetivo=-1, peso_paridad=2.3,
            )
        self.assertIs(mejor, menor_costo)
        self.assertTrue(all(c.kwargs["paridad_objetivo"] == -1 for c in ejecutar.call_args_list))
        self.assertTrue(all(c.kwargs["peso_paridad"] == 2.3 for c in ejecutar.call_args_list))

    def test_rechaza_configuracion_invalida(self):
        parametros = np.zeros((2, 2, 3))
        for objetivo, peso in ((0, 1.0), (1, -1.0), (1, np.nan), (1, np.inf)):
            with self.subTest(objetivo=objetivo, peso=peso):
                with self.assertRaises(ValueError):
                    self.ejecutar(parametros, objetivo=objetivo, peso=peso)


if __name__ == "__main__":
    unittest.main()
