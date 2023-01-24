from math import sqrt
from uuid import UUID

from tortoise import transactions

from code.game.structures import Point
from code.models import Game


def get_distance_between_points(a: Point, b: Point) -> float:
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


async def get_game(game_id: UUID) -> Game | None:
    return await Game.get_or_none(id=game_id, status=Game.Status.NEW).select_related('user')


async def update_game_status(game: Game, status: Game.Status) -> None:
    game.status = status
    await game.save(update_fields=['status'])


async def update_game_score(game: Game, score: int) -> None:
    game.score = score
    await game.save(update_fields=['score'])


async def finish_game(game: Game, score: int) -> None:
    async with transactions.in_transaction():
        await update_game_status(game, Game.Status.FINISHED)
        await update_game_score(game, score)
