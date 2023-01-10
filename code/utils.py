from random import randint

from code import consts


def generate_radius() -> int:
    return randint(consts.MINIMUM_METEOR_RADIUS, consts.MAXIMUM_METEOR_RADIUS)


def generate_degree() -> int:
    return randint(consts.MINIMUM_DEGREE, consts.MAXIMUM_DEGREE)
