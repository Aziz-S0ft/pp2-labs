import random


def random_float() -> float:
    return random.random()


def random_integer(a: int, b: int) -> int:
    return random.randint(a, b)


def random_choice(elements: list):
    return random.choice(elements)


def shuffle_list(elements: list) -> list:
    random.shuffle(elements)
    return elements


def random_uniform(a: float, b: float) -> float:
    return random.uniform(a, b)


if __name__ == "__main__":
    print("Random float:", random_float())
    print("Random int:", random_integer(1, 10))
    print("Choice:", random_choice(["a", "b", "c"]))
    print("Shuffle:", shuffle_list([1, 2, 3, 4]))
    print("Uniform:", random_uniform(1.5, 5.5))