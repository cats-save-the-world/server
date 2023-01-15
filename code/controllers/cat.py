from code.consts import CAT_RADIUS, CatDirection, CatStatus, ControlActionType, PLANET_DISTANCE
from ._rotatable import RotatableController


class CatController(RotatableController):
    ACCELERATION_SPEED: int = 2
    BRAKING_SPEED: int = 1
    MAX_SPEED: int = 10

    def __init__(self) -> None:
        super().__init__(angle=0, distance=PLANET_DISTANCE, radius=CAT_RADIUS)
        self._speed: int = 0
        self._status: CatStatus = CatStatus.IDLE
        self._direction: CatDirection = CatDirection.RIGHT
        self._control_action: ControlActionType = ControlActionType.STOP

    @property
    def state(self) -> dict:
        return {
            'angle': self._angle,
            'status': self._status,
            'direction': self._direction,
        }

    @property
    def control_action(self) -> ControlActionType:
        return self._control_action

    @control_action.setter
    def control_action(self, value: ControlActionType) -> None:
        self._control_action = value

        if value == ControlActionType.LEFT:
            self._direction = CatDirection.LEFT
        elif value == ControlActionType.RIGHT:
            self._direction = CatDirection.RIGHT

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    def _update_speed(self) -> None:
        if self._control_action == ControlActionType.RIGHT:
            self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif self._control_action == ControlActionType.LEFT:
            self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)

        elif self._control_action == ControlActionType.STOP:
            if self._speed > 0:
                self._speed = max(self._speed - self.BRAKING_SPEED, 0)
            else:
                self._speed = min(self._speed + self.BRAKING_SPEED, 0)

    def _update_status(self) -> None:
        self._status = CatStatus.IDLE if self._speed == 0 else CatStatus.RUNNING

    def _update_angle(self) -> None:
        self._angle += self._speed

    def tick(self) -> None:
        self._update_speed()
        self._update_status()
        self._update_angle()
