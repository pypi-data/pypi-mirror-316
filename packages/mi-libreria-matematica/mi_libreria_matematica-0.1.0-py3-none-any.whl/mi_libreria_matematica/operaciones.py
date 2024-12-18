# src/mi_libreria_matematica/operaciones.py

def sumar(a, b):
    """Devuelve la suma de dos números."""
    return a + b

def restar(a, b):
    """Devuelve la resta de dos números."""
    return a - b

def multiplicar(a, b):
    """Devuelve la multiplicación de dos números."""
    return a * b

def dividir(a, b):
    """Devuelve la división de dos números."""
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a / b