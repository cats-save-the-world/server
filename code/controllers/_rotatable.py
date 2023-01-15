from math import cos, radians, sin

from code.structures import Point
from code.utils import get_distance_between_points


class RotatableController:
    radius: int

    def __init__(self, angle: float, distance: int) -> None:
        self._angle = angle
        self.distance = distance

    @property
    def center(self) -> Point:
        angle = radians(self._angle)
        distance = self.distance + self.radius
        return Point(sin(angle) * distance, cos(angle) * distance)

    @property
    def state(self) -> dict:
        return {
            'angle': self._angle,
            'distance': self.distance,
        }

    def intersects(self, other: 'RotatableController') -> bool:
        return self.radius + other.radius > get_distance_between_points(self.center, other.center)
