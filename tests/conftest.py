from typing import AsyncGenerator

from httpx import AsyncClient
import pytest
from tortoise import Tortoise

from code.app import app
from code.auth.utils import get_password_hash
from code.config import TEST_TORTOISE_CONFIG
from code.models import User


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


@pytest.fixture
async def user() -> User:
    return await User.create(username='username', password_hash=get_password_hash('password'))
