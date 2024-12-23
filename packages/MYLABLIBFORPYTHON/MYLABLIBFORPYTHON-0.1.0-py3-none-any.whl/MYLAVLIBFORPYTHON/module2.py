def multiply(a, b):
    """Функция для умножения двух чисел"""
    return a * b

def divide(a, b):
    """Функция для деления двух чисел"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b
