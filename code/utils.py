from random import randint


MINIMUM_GENERATION_RADIUS = 450
MAXIMUM_GENERATION_RADIUS = 600

MINIMUM_DEGREE = 0
MAXIMUM_DEGREE = 359


def generate_radius() -> int:
    return randint(MINIMUM_GENERATION_RADIUS, MAXIMUM_GENERATION_RADIUS)


def generate_degree() -> int:
    return randint(MINIMUM_DEGREE, MAXIMUM_DEGREE)
