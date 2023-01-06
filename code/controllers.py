from abc import ABC, abstractmethod

from code.consts import ControlActionTypes, GameEventTypes


class Controller(ABC):
    @property
    @abstractmethod
    def state(self) -> dict: ...


class CatController(Controller):
    ACCELERATION_SPEED: int = 2
    BRAKING_SPEED: int = 1
    _degree: int = 0
    _speed: int = 0

    @property
    def state(self) -> dict:
        return {
            'degree': self._degree,
        }

    def control(self, control_action_type: ControlActionTypes):
        if control_action_type == ControlActionTypes.LEFT:
            self._degree -= self.ACCELERATION_SPEED
        elif control_action_type == ControlActionTypes.RIGHT:
            self._degree += self.ACCELERATION_SPEED
        elif control_action_type == ControlActionTypes.STOP:
            self._degree = 0


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
