import math


def square_root(x: float) -> float:
    return math.sqrt(x)


def factorial(n: int) -> int:
    return math.factorial(n)


def ceil_value(x: float) -> float:
    return math.ceil(x)


def floor_value(x: float) -> float:
    return math.floor(x)


def logarithm(x: float, base: float = math.e) -> float:
    return math.log(x, base)


if __name__ == "__main__":
    print("Sqrt:", square_root(16))
    print("Factorial:", factorial(5))
    print("Ceil:", ceil_value(3.2))
    print("Floor:", floor_value(3.8))
    print("Log:", logarithm(10))