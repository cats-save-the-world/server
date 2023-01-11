from abc import ABC, abstractmethod
import asyncio

from code.consts import ControlActionTypes, GameEventTypes

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


class GameController(Controller):
    _cat: CatController
    _last_control_action: str = ControlActionTypes.STOP
    _cycle_task: asyncio.Task

    def __init__(self) -> None:
        self._cat = CatController()
        self._cycle_task = asyncio.create_task(self._cycle())

    async def _cycle(self) -> None:
        while True:
            self._cat.control(self._last_control_action)
            await asyncio.sleep(CYCLE_INTERVAL)

    def stop_cycle(self) -> None:
        self._cycle_task.cancel()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
        }

    def dispatch(self, action: dict) -> None:
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._last_control_action = action['payload']
