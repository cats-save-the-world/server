from random import randint
from typing import Callable
from uuid import UUID, uuid4

from code.consts import PLANET_DISTANCE
from ._rotatable import RotatableController


class EnemyController(RotatableController):
    SPEED: int = 10
    MAX_DISTANCE: int = 1000
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 359

    def __init__(self, remove: Callable) -> None:
        super().__init__(
            angle=randint(self.MIN_ANGLE, self.MAX_ANGLE),
            distance=self.MAX_DISTANCE,
        )
        self.id: UUID = uuid4()
        self._remove: Callable = remove

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'distance': self._distance,
            'angle': self._angle,
        }

    def tick(self) -> None:
        self._distance -= self.SPEED

        if self._distance < PLANET_DISTANCE:
            self._remove(self.id)
