import pytest

from code.game.structures import Point
from code.game.utils import get_distance_between_points, finish_game, get_game, update_game_status
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


async def test_update_game_status_new(active_game: Game) -> None:
    await update_game_status(active_game, Game.Status.NEW)
    assert active_game.status == Game.Status.NEW


async def test_update_game_status_active(new_game: Game) -> None:
    await update_game_status(new_game, Game.Status.ACTIVE)
    assert new_game.status == Game.Status.ACTIVE


async def test_update_game_status_finished(new_game: Game) -> None:
    await update_game_status(new_game, Game.Status.FINISHED)
    assert new_game.status == Game.Status.FINISHED


async def test_finish_game_with_score(active_game: Game) -> None:
    await finish_game(active_game, 3000)

    assert active_game.status == Game.Status.FINISHED
    assert active_game.score == 3000


async def test_finish_game_without_score(active_game: Game) -> None:
    await finish_game(active_game)

    assert active_game.status == Game.Status.FINISHED
    assert active_game.score is None
