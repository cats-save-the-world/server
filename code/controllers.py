import asyncio
from abc import ABC, abstractmethod
from typing import List

from uuid import uuid4 as generate_uuid

from code.consts import ControlActionTypes, GameEventTypes, METEOR_GENERATION_INTERVAL, MAX_METEOR_NUMBER
from code.utils import generate_degree, generate_radius


class Controller(ABC):
    @property
    @abstractmethod
    def state(self) -> dict: ...


class CatController(Controller):
    ACCELERATION_SPEED: int = 1
    BRAKING_SPEED: int = 0.5
    MAX_SPEED: int = 10
    _degree: int = 0
    _speed: int = 0

    @property
    def state(self) -> dict:
        return {
            'degree': self._degree,
        }

    def control(self, control_action_type: ControlActionTypes):
        self._degree += self._speed

        if control_action_type == ControlActionTypes.RIGHT:
            if self._speed > 0:
                self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)
            else:
                self._speed += self.BRAKING_SPEED

        elif control_action_type == ControlActionTypes.LEFT:
            if self._speed > 0:
                self._speed -= self.BRAKING_SPEED
            else:
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
    _meteors: List[MeteorController] = []

    def __init__(self) -> None:
        self._cat = CatController()
        self.generate_meteor_task = asyncio.create_task(self.generate_meteor())

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'meteors': [meteor.state for meteor in self._meteors],
        }

    def dispatch(self, action: dict):
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._cat.control(action['payload'])

        for meteor in self._meteors:
            meteor.control()

    async def generate_meteor(self):
        while True:
            if len(self._meteors) < MAX_METEOR_NUMBER:
                self._meteors.append(MeteorController())
            await asyncio.sleep(METEOR_GENERATION_INTERVAL)
