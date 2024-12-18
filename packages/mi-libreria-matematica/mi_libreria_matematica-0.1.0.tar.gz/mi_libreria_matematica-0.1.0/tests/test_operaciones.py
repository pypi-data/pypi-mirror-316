# tests/test_operaciones.py
import unittest
from mi_libreria_matematica.operaciones import sumar, restar, multiplicar, dividir

class TestOperacionesMatematicas(unittest.TestCase):
    def test_sumar(self):
        self.assertEqual(sumar(2, 3), 5)

    def test_restar(self):
        self.assertEqual(restar(5, 3), 2)

    def test_multiplicar(self):
        self.assertEqual(multiplicar(2, 3), 6)

    def test_dividir(self):
        self.assertEqual(dividir(6, 3), 2)
        with self.assertRaises(ValueError):
            dividir(6, 0)

if __name__ == "__main__":
    unittest.main()