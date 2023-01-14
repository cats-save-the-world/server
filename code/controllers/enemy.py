from random import randint
from uuid import UUID, uuid4

from ._rotatable import RotatableController


class EnemyController(RotatableController):
    SPEED: int = 10
    MAX_DISTANCE: int = 1000
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 359
    DAMAGE: int = 5

    def __init__(self) -> None:
        super().__init__(
            angle=randint(self.MIN_ANGLE, self.MAX_ANGLE),
            distance=self.MAX_DISTANCE,
        )
        self.id: UUID = uuid4()
        self.damage = self.DAMAGE

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'distance': self._distance,
            'angle': self._angle,
        }

    def tick(self) -> None:
        self._distance -= self.SPEED
