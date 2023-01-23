from typing import AsyncGenerator

from httpx import AsyncClient
import pytest
from tortoise import Tortoise

from code.app import app
from code.config import TEST_TORTOISE_CONFIG


@pytest.fixture
async def database() -> AsyncGenerator:
    await Tortoise.init(config=TEST_TORTOISE_CONFIG, _create_db=True)
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest.fixture
async def client(database: None) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
