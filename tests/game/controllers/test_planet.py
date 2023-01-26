import pytest

from code.game.controllers.planet import PlanetController
from code.game.exceptions import GameOver


@pytest.mark.parametrize('health, damage', [
    (PlanetController.MAX_HEALTH, 0),
    (PlanetController.MAX_HEALTH / 2, 0.5),
    (0, 1),
])
def test_state(health: int, damage: int) -> None:
    controller = PlanetController()
    controller._health = health
    assert controller.state['damage'] == damage


def test_get_damage_full() -> None:
    controller = PlanetController()

    with pytest.raises(GameOver):
        controller.get_damage(PlanetController.MAX_HEALTH)

    assert controller._health == 0


@pytest.mark.parametrize(
    'damage, heal, has_exception, result_health', [
        (30, 10, False, 80),
        (50, 50, False, 100),
        (70, 20, False, 50),
        (100, 10, True, 0),
    ],
)
def test_get_heal(damage: int, heal: int, has_exception: bool, result_health: int) -> None:
    controller = PlanetController()

    if has_exception:
        with pytest.raises(GameOver):
            controller.get_damage(damage)
            controller.get_heal(heal)

    else:
        controller.get_damage(damage)
        controller.get_heal(heal)

    assert controller._health == result_health


def test_get_max_heal() -> None:
    controller = PlanetController()

    controller.get_heal(15)
    assert controller._health == PlanetController.MAX_HEALTH
