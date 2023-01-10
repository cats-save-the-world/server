from abc import ABC, abstractmethod

from code.consts import ControlActionTypes, GameEventTypes


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

        if control_action_type == ControlActionTypes.LEFT:
            if self._speed <= 0:
                self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)
            else:
                self._speed = min(self._speed - self.BRAKING_SPEED, self.MAX_SPEED)

        elif control_action_type == ControlActionTypes.RIGHT:
            if self._speed <= 0:
                self._speed = min(self._speed + self.BRAKING_SPEED, self.MAX_SPEED)
            else:
                self._speed = max(self._speed - self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif control_action_type == ControlActionTypes.STOP:
            if self._speed <= 0:
                self._speed = min(self._speed + self.BRAKING_SPEED, 0)
            else:
                self._speed = max(self._speed - self.BRAKING_SPEED, 0)


class GameController(Controller):
    _cat: CatController

    def __init__(self) -> None:
        self._cat = CatController()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
        }

    def dispatch(self, action: dict):
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._cat.control(action['payload'])
