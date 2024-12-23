"""This module contains basic arithmetic operations: addition, subtraction, multiplication, and division."""


def add(a: int | float, b: int | float) -> int | float:
    """
    Adds two numbers.

    Args:
        a (int | float): The first number.
        b (int | float): The second number.

    Returns:
        int | float: The sum of the two numbers. The return type will be either int or float, depending on the input types.
    """
    return a + b


def subtract(a: int | float, b: int | float) -> int | float:
    """
    Subtracts the second number from the first.

    Args:
        a (int | float): The number to subtract from.
        b (int | float): The number to subtract.

    Returns:
        int | float: The result of the subtraction. The return type will be either int or float, depending on the input types.
    """
    return a - b


def multiply(a: int | float, b: int | float) -> int | float:
    """
    Multiplies two numbers.

    Args:
        a (int | float): The first number.
        b (int | float): The second number.

    Returns:
        int | float: The product of the two numbers. The return type will be either int or float, depending on the input types.
    """
    return a * b


def divide(a: int | float, b: int | float) -> float:
    """
    Divides the first number by the second.

    Args:
        a (int | float): The numerator.
        b (int | float): The denominator.

    Returns:
        float: The result of the division, always of type float.

    Raises:
        ValueError: If the denominator (b) is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")

    return a / b
