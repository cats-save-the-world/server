from math import sqrt
from uuid import UUID

from code.game.exceptions import AlreadyInGame
from code.game.structures import Point
from code.models import Game, User


def get_distance_between_points(a: Point, b: Point) -> float:
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


async def get_game(game_id: UUID) -> Game | None:
    return await Game.get_or_none(id=game_id, status=Game.Status.NEW).select_related('user')


async def update_game_status(game: Game, status: Game.Status) -> None:
    game.status = status
    await game.save(update_fields=['status'])


async def finish_game(game: Game, score: int | None = None) -> None:
    game.score = score
    game.status = Game.Status.FINISHED
    await game.save(update_fields=['score', 'status'])


async def create_game(user: User) -> Game:
    if await Game.filter(user=user, status=Game.Status.ACTIVE).exists():
        raise AlreadyInGame

    game, _ = await Game.get_or_create(user=user, status=Game.Status.NEW)

    return game
