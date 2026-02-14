def absolute_value(x: float) -> float:
    return abs(x)


def rounded_value(x: float, digits: int = 0) -> float:
    return round(x, digits)


def power(base: float, exponent: float) -> float:
    return pow(base, exponent)


def min_value(numbers: list) -> float:
    return min(numbers)


def max_value(numbers: list) -> float:
    return max(numbers)


if __name__ == "__main__":
    print("Abs:", absolute_value(-10))
    print("Round:", rounded_value(3.14159, 2))
    print("Power:", power(2, 3))
    print("Min:", min_value([3, 1, 7]))
    print("Max:", max_value([3, 1, 7]))
