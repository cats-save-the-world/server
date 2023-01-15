from random import choice, uniform
from uuid import UUID, uuid4

from ._rotatable import RotatableController


class EnemyController(RotatableController):
    INITIAL_DISTANCE: int = 1000
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 359
    damage: int
    speed: int
    type: str  # noqa: A003

    def __init__(self) -> None:
        angle = round(uniform(self.MIN_ANGLE, self.MAX_ANGLE), 2)
        super().__init__(angle=angle, distance=self.INITIAL_DISTANCE)
        self.id: UUID = uuid4()

    @property
    def state(self) -> dict:
        return {
            **super().state,
            'id': str(self.id),
            'distance': self.distance,
            'type': self.type,
        }

    def tick(self) -> None:
        self.distance -= self.speed


class SimpleEnemyController(EnemyController):
    speed: int = 10
    radius: int = 10
    damage: int = 10
    type: str = 'simple'  # noqa: A003


class HeavyEnemyController(EnemyController):
    speed: int = 5
    radius: int = 20
    damage: int = 20
    type: str = 'heavy'  # noqa: A003


class LightEnemyController(EnemyController):
    speed: int = 20
    radius: int = 10
    damage: int = 5
    type: str = 'light'  # noqa: A003


class TwistedEnemyController(EnemyController):
    ANGLE_SHIFT: float = 0.5
    speed: int = 10
    radius: int = 10
    damage: int = 10
    type: str = 'twisted'  # noqa: A003

    def __init__(self) -> None:
        super().__init__()
        self._angle_shift: float = choice([self.ANGLE_SHIFT, -self.ANGLE_SHIFT])

    def tick(self) -> None:
        super().tick()
        self._angle += self._angle_shift
