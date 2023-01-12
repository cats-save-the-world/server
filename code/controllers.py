from abc import ABC, abstractmethod
import asyncio
from uuid import uuid4

from code.consts import ControlActionTypes, GameEventTypes
from code.utils import generate_degree, generate_radius

CYCLE_INTERVAL = 0.1


class Controller(ABC):
    @property
    @abstractmethod
    def state(self) -> dict: ...


class CatController(Controller):
    ACCELERATION_SPEED: int = 2
    BRAKING_SPEED: int = 1
    MAX_SPEED: int = 10
    _degree: int = 0
    _speed: int = 0

    @property
    def state(self) -> dict:
        return {
            'degree': self._degree,
        }

    def control(self, control_action_type: str) -> None:
        self._degree += self._speed

        if control_action_type == ControlActionTypes.RIGHT:
            self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif control_action_type == ControlActionTypes.LEFT:
            self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)

        elif control_action_type == ControlActionTypes.STOP:
            if self._speed > 0:
                self._speed = max(self._speed - self.BRAKING_SPEED, 0)
            else:
                self._speed = min(self._speed + self.BRAKING_SPEED, 0)


class EnemyController(Controller):
    SPEED: int = 10

    def __init__(self):
        self.id = uuid4()
        self._radius = generate_radius()
        self._degree = generate_degree()

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'radius': self._radius,
            'degree': self._degree,
        }

    def control(self):
        self._radius -= self.SPEED

        if self._radius <= 150:
            pass
            #  TODO достиг Земли


class EnemiesController(Controller):
    ENEMY_GENERATION_INTERVAL: int = 3
    _enemies: dict

    def __init__(self) -> None:
        self._enemies = {}
        self._generate_enemies_task = asyncio.create_task(self.generate_enemies())

    async def generate_enemies(self):
        while True:
            enemy = EnemyController()
            self._enemies[enemy.state['id']] = enemy
            await asyncio.sleep(self.ENEMY_GENERATION_INTERVAL)

    def stop_generate_enemies(self):
        self._generate_enemies_task.cancel()

    def control(self):
        for enemy in self._enemies.values():
            enemy.control()

    @property
    def state(self) -> list:
        return [enemy.state for enemy in self._enemies.values()]


class GameController(Controller):
    _cat: CatController
    _last_control_action: str = ControlActionTypes.STOP
    _cycle_task: asyncio.Task
    _enemies: EnemiesController

    def __init__(self) -> None:
        self._cat = CatController()
        self._enemies = EnemiesController()
        self._cycle_task = asyncio.create_task(self._cycle())

    async def _cycle(self) -> None:
        while True:
            self._cat.control(self._last_control_action)
            self._enemies.control()
            await asyncio.sleep(CYCLE_INTERVAL)

    def stop_cycle(self) -> None:
        self._enemies.stop_generate_enemies()
        self._cycle_task.cancel()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
        }

    def dispatch(self, action: dict) -> None:
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._last_control_action = action['payload']
