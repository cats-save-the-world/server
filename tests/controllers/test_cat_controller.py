import pytest

from code.consts import ControlActionTypes
from code.controllers import CatController


def _reach_max_speed(controller: CatController, control_action: str):
    max_speed = CatController.MAX_SPEED

    if control_action == 'left':
        max_speed *= -1

    while controller._speed != max_speed:
        controller.control(control_action)


@pytest.mark.parametrize('control_action, expected_speed', [
    (ControlActionTypes.LEFT, -CatController.ACCELERATION_SPEED),
    (ControlActionTypes.RIGHT, CatController.ACCELERATION_SPEED),
])
def test_start_move(control_action: str, expected_speed: int):
    controller = CatController()
    controller.control(control_action)

    assert controller._speed == expected_speed


@pytest.mark.parametrize('control_action, expected_speed', [
    (ControlActionTypes.LEFT, -CatController.MAX_SPEED),
    (ControlActionTypes.RIGHT, CatController.MAX_SPEED),
])
def test_max_speed(control_action: str, expected_speed: int):
    controller = CatController()
    _reach_max_speed(controller, control_action)
    controller.control(control_action)

    assert controller._speed == expected_speed


@pytest.mark.parametrize('control_action, expected_speed', [
    (ControlActionTypes.LEFT, -CatController.ACCELERATION_SPEED + CatController.BRAKING_SPEED),
    (ControlActionTypes.RIGHT, CatController.ACCELERATION_SPEED - CatController.BRAKING_SPEED),
])
def test_stop(control_action: str, expected_speed: int):
    controller = CatController()
    controller.control(control_action)
    controller.control(ControlActionTypes.STOP)

    assert controller._speed == expected_speed
