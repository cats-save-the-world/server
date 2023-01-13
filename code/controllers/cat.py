from code.consts import CatDirection, CatStatus, ControlActionTypes
from ._base import BaseController


class CatController(BaseController):
    ACCELERATION_SPEED: int = 2
    BRAKING_SPEED: int = 1
    MAX_SPEED: int = 10

    def __init__(self) -> None:
        self._degree: int = 0
        self._speed: int = 0
        self._status: str = CatStatus.IDLE
        self._direction: str = CatDirection.RIGHT
        self._control_action: str = ControlActionTypes.STOP

    @property
    def state(self) -> dict:
        return {
            'degree': self._degree,
            'status': self._status,
            'direction': self._direction,
        }

    @property
    def control_action(self) -> str:
        return self._control_action

    @control_action.setter
    def control_action(self, value: str) -> None:
        self._control_action = value

        if value == ControlActionTypes.LEFT:
            self._direction = CatDirection.LEFT
        elif value == ControlActionTypes.RIGHT:
            self._direction = CatDirection.RIGHT

    def _update_speed(self) -> None:
        if self._control_action == ControlActionTypes.RIGHT:
            self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif self._control_action == ControlActionTypes.LEFT:
            self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)

        elif self._control_action == ControlActionTypes.STOP:
            if self._speed > 0:
                self._speed = max(self._speed - self.BRAKING_SPEED, 0)
            else:
                self._speed = min(self._speed + self.BRAKING_SPEED, 0)

    def _update_status(self) -> None:
        self._status = CatStatus.IDLE if self._speed == 0 else CatStatus.RUNNING

    def tick(self) -> None:
        self._update_speed()
        self._update_status()
        self._degree += self._speed
