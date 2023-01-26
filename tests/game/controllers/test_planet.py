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


def test_get_heal() -> None:
    controller = PlanetController()

    controller.get_damage(30)
    assert controller._health == 70

    controller.get_heal(10)

    assert controller._health == 80


def test_get_max_heal() -> None:
    controller = PlanetController()

    controller.get_heal(15)
    assert controller._health == PlanetController.MAX_HEALTH
