from random import choice, uniform
from uuid import uuid4

from ._circle import CircleController


class EnemyController(CircleController):
    INITIAL_DISTANCE = 1000
    MIN_ANGLE = 0
    MAX_ANGLE = 359
    damage: int
    speed: int
    type: str  # noqa: A003
    score: int

    def __init__(self) -> None:
        angle = round(uniform(self.MIN_ANGLE, self.MAX_ANGLE), 2)
        super().__init__(angle=angle, distance=self.INITIAL_DISTANCE)
        self.id = uuid4()

    @property
    def state(self) -> dict:
        return {
            **super().state,
            'id': str(self.id),
            'type': self.type,
        }

    def tick(self) -> None:
        self.distance -= self.speed


class SimpleEnemyController(EnemyController):
    speed = 10
    radius = 10
    damage = 10
    type = 'simple'  # noqa: A003
    score = 100


class HeavyEnemyController(EnemyController):
    speed = 5
    radius = 20
    damage = 20
    type = 'heavy'  # noqa: A003
    score = 150


class LightEnemyController(EnemyController):
    speed = 20
    radius = 10
    damage = 5
    type = 'light'  # noqa: A003
    score = 200


class TwistedEnemyController(EnemyController):
    ANGLE_SHIFT = 0.5
    speed = 10
    radius = 10
    damage = 10
    type = 'twisted'  # noqa: A003
    score = 150

    def __init__(self) -> None:
        super().__init__()
        self._angle_shift = choice([self.ANGLE_SHIFT, -self.ANGLE_SHIFT])

    def tick(self) -> None:
        super().tick()
        self._angle += self._angle_shift
