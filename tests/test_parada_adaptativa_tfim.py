import unittest

from scripts.continuar_tfim_adaptativo import decidir_parada


class ParadaAdaptativaTFIMTests(unittest.TestCase):
    def test_objetivo_tiene_prioridad(self):
        row = {"fidelidad": 0.991, "costo_medio": -7.0, "paso": 100}
        self.assertEqual(decidir_parada(row, None), "fidelidad_objetivo")

    def test_estancamiento_requiere_dos_cambios_consecutivos(self):
        prior = None
        for step, expected in ((100, None), (200, None), (300, "estancamiento")):
            row = {"fidelidad": 0.98 + step * 1e-8, "costo_medio": -7.0, "paso": step}
            self.assertEqual(decidir_parada(row, prior), expected)
            prior = row

    def test_cambio_importante_de_fidelidad_reinicia_el_contador(self):
        prior = {"fidelidad": 0.98, "costo_medio": -7.0, "bloques_estables": 1}
        row = {"fidelidad": 0.96, "costo_medio": -7.0, "paso": 300}
        self.assertIsNone(decidir_parada(row, prior))
        self.assertEqual(row["bloques_estables"], 0)

    def test_la_perdida_media_tambien_debe_ser_estable(self):
        prior = {"fidelidad": 0.98, "costo_medio": -7.0, "bloques_estables": 1}
        row = {"fidelidad": 0.98, "costo_medio": -7.01, "paso": 300}
        self.assertIsNone(decidir_parada(row, prior))
        self.assertEqual(row["bloques_estables"], 0)

    def test_limite_y_umbral_estricto(self):
        row = {"fidelidad": 0.99, "costo_medio": -7.0, "paso": 800}
        self.assertEqual(decidir_parada(row, None), "limite_pasos")


if __name__ == "__main__":
    unittest.main()
