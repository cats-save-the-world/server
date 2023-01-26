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


@pytest.mark.parametrize('heal, health', [
    (0, 0),
    (10, 10),
    (PlanetController.MAX_HEALTH, PlanetController.MAX_HEALTH),
])
def test_get_heal(heal: int, health: int) -> None:
    controller = PlanetController()
    controller._health = 0
    controller.get_heal(heal)
    assert controller._health == health


@pytest.mark.parametrize('heal, health', [
    (0, PlanetController.MAX_HEALTH),
    (10, PlanetController.MAX_HEALTH),
    (PlanetController.MAX_HEALTH, PlanetController.MAX_HEALTH),
])
def test_get_heal_full(heal: int, health: int) -> None:
    controller = PlanetController()
    controller.get_heal(heal)
    assert controller._health == health
