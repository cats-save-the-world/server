from math import cos, radians, sin

from code.structures import Point
from code.utils import get_distance_between_points


class RotatableController:
    def __init__(self, angle: int, distance: int, radius: int) -> None:
        self._angle: int = angle
        self.distance: int = distance
        self.radius: int = radius

    @property
    def center(self) -> Point:
        angle = radians(self._angle)
        distance = self.distance + self.radius
        return Point(sin(angle) * distance, cos(angle) * distance)

    def intersects(self, other: 'RotatableController') -> bool:
        return self.radius + other.radius > get_distance_between_points(self.center, other.center)
