import pytest

from code.models import Game


@pytest.fixture
async def new_game(database: None) -> Game:
    return await Game.create(status=Game.Status.NEW)


@pytest.fixture
async def active_game(database: None) -> Game:
    return await Game.create(status=Game.Status.ACTIVE)
