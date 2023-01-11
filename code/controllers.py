from abc import ABC, abstractmethod
import asyncio
from typing import List
from uuid import uuid4 as generate_uuid

from code.consts import ControlActionTypes, GameEventTypes, MAX_METEORS, METEOR_GENERATION_INTERVAL
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


class MeteorController(Controller):
    SPEED: int = 10

    def __init__(self):
        self.id = str(generate_uuid())
        self._radius = generate_radius()
        self._degree = generate_degree()

    @property
    def state(self) -> dict:
        return {
            'id': self.id,
            'radius': self._radius,
            'degree': self._degree,
        }

    def control(self):
        self._radius -= self.SPEED

        if self._radius <= 150:
            pass
            #  TODO метеорит достиг Земли


class GameController(Controller):
    _cat: CatController
    _last_control_action: str = ControlActionTypes.STOP
    _cycle_task: asyncio.Task
    _meteors: List[MeteorController] = []

    def __init__(self) -> None:
        self._cat = CatController()
        self._cycle_task = asyncio.create_task(self._cycle())
        self._generate_meteors_task = asyncio.create_task(self.generate_meteors())

    async def _cycle(self) -> None:
        while True:
            self._cat.control(self._last_control_action)
            self.control_meteors()
            await asyncio.sleep(CYCLE_INTERVAL)

    def stop_cycle(self) -> None:
        self._cycle_task.cancel()

    async def generate_meteors(self):
        while True:
            if len(self._meteors) < MAX_METEORS:
                self._meteors.append(MeteorController())
            await asyncio.sleep(METEOR_GENERATION_INTERVAL)

    def stop_generate_meteor(self):
        self._generate_meteors_task.cancel()

    def control_meteors(self):
        for meteor in self._meteors:
            meteor.control()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'meteors': [meteor.state for meteor in self._meteors],
        }

    def dispatch(self, action: dict) -> None:
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._last_control_action = action['payload']
