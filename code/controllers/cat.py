from code.consts import CAT_RADIUS, CatDirection, CatStatus, ControlAction, PLANET_DISTANCE
from ._rotatable import RotatableController


class CatController(RotatableController):
    ACCELERATION_SPEED = 2
    BRAKING_SPEED = 1
    MAX_SPEED = 10
    radius = CAT_RADIUS

    def __init__(self) -> None:
        super().__init__(angle=0, distance=PLANET_DISTANCE)
        self._speed = 0
        self._status = CatStatus.IDLE
        self._direction = CatDirection.RIGHT
        self._control_action = ControlAction.STOP

    @property
    def state(self) -> dict:
        return {
            **super().state,
            'status': self._status,
            'direction': self._direction,
        }

    @property
    def control_action(self) -> ControlAction:
        return self._control_action

    @control_action.setter
    def control_action(self, value: ControlAction) -> None:
        self._control_action = value

        if value == ControlAction.LEFT:
            self._direction = CatDirection.LEFT
        elif value == ControlAction.RIGHT:
            self._direction = CatDirection.RIGHT

    @property
    def status(self) -> CatStatus:
        return self._status

    @status.setter
    def status(self, value: CatStatus) -> None:
        self._status = value

    def _update_speed(self) -> None:
        if self._control_action == ControlAction.RIGHT:
            self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif self._control_action == ControlAction.LEFT:
            self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)

        elif self._control_action == ControlAction.STOP:
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
