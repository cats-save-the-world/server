from math import cos, radians, sin

from code.structures import Point
from code.utils import get_distance_between_points


class RotatableController:
    RADIUS: int = 10

    def __init__(self, angle: int, distance: int) -> None:
        self._angle: int = angle
        self._distance: int = distance

    @property
    def center(self) -> Point:
        angle = radians(self._angle)
        distance = self._distance + self.RADIUS
        return Point(sin(angle) * distance, cos(angle) * distance)

    def intersect(self, other: 'RotatableController') -> bool:
        return self.RADIUS + other.RADIUS > get_distance_between_points(self.center, other.center)
