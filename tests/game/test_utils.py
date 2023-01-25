import pytest

from code.game.structures import Point
from code.game.utils import get_distance_between_points, get_game
from code.models import Game


@pytest.mark.parametrize(
    'a, b, distance',
    [
        (Point(x=0, y=0), Point(x=3, y=4), 5.0),
        (Point(x=3, y=7), Point(x=-11, y=12), 14.87),
        (Point(x=-5, y=-8), Point(x=44, y=85), 105.12),
    ],
)
def test_get_distance_between_points(a: Point, b: Point, distance: float) -> None:
    assert round(get_distance_between_points(a, b), 2) == distance


async def test_get_game(new_game: Game, active_game: Game) -> None:
    assert await get_game(new_game.id) == new_game
    assert await get_game(active_game.id) is None
