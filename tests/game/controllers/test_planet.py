import pytest

from code.game.controllers.planet import PlanetController


@pytest.mark.parametrize('health, damage', [
    (PlanetController.MAX_HEALTH, 0),
    (PlanetController.MAX_HEALTH / 2, 0.5),
    (0, 1),
])
def test_damage(health: int, damage: int) -> None:
    controller = PlanetController()
    controller._health = health

    assert controller.state['damage'] == damage