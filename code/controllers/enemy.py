from random import randint
from uuid import UUID, uuid4

from ._rotatable import RotatableController


class EnemyController(RotatableController):
    MAX_DISTANCE: int = 1000
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 359
    DAMAGE: int = 10

    def __init__(self, radius: int, speed: int, damage: int, angle_shift: int, type: str) -> None:  # noqa
        super().__init__(
            angle=randint(self.MIN_ANGLE, self.MAX_ANGLE),
            distance=self.MAX_DISTANCE,
            radius=radius,
        )
        self.id: UUID = uuid4()
        self._speed: int = speed
        self.damage: int = damage
        self._angle_shift: int = angle_shift
        self._type: str = type

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'distance': self.distance,
            'angle': self._angle,
            'type': self._type,
        }

    def tick(self) -> None:
        self.distance -= self._speed
        self._angle += self._angle_shift
