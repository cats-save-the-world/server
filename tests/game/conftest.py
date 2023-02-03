import pytest

from code.models import Game, User


@pytest.fixture
async def new_game(database: None) -> Game:
    return await Game.create(status=Game.Status.NEW)


@pytest.fixture
async def active_game(database: None) -> Game:
    return await Game.create(status=Game.Status.ACTIVE)


@pytest.fixture
async def finished_game(database: None) -> Game:
    return await Game.create(status=Game.Status.FINISHED)


@pytest.fixture
async def finished_game_with_user(database: None, user: User) -> Game:
    return await Game.create(status=Game.Status.FINISHED, user=user)
