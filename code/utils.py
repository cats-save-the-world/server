from math import sqrt

from code.structures import Point


def get_distance_between_points(a: Point, b: Point) -> float:
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
