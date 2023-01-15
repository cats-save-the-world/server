from random import randint
from uuid import UUID, uuid4

from ._rotatable import RotatableController


class EnemyController(RotatableController):
    MAX_DISTANCE: int = 1000
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 359
    DAMAGE: int = 10
    TYPE: str
    RADIUS: int
    SPEED: int

    def __init__(self) -> None:
        super().__init__(
            angle=randint(self.MIN_ANGLE, self.MAX_ANGLE),
            distance=self.MAX_DISTANCE,
            radius=self.RADIUS,
        )
        self.id: UUID = uuid4()
        self._speed: int = self.SPEED

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'distance': self.distance,
            'angle': self._angle,
            'type': self.TYPE,
        }

    def tick(self) -> None:
        self.distance -= self._speed


class SimpleEnemyController(EnemyController):
    SPEED: int = 10
    RADIUS: int = 10
    DAMAGE: int = 10
    TYPE: str = 'simple'


class HeavyEnemyController(EnemyController):
    SPEED: int = 5
    RADIUS: int = 20
    DAMAGE: int = 20
    TYPE: str = 'heavy'


class LightEnemyController(EnemyController):
    SPEED: int = 20
    RADIUS: int = 5
    DAMAGE: int = 5
    TYPE: str = 'light'


class TwistEnemyController(EnemyController):
    SPEED: int = 10
    RADIUS: int = 10
    DAMAGE: int = 10
    ANGLE_SHIFT: float = 0.5
    TYPE: str = 'twist'

    def tick(self) -> None:
        super().tick()
        self._angle += self.ANGLE_SHIFT
