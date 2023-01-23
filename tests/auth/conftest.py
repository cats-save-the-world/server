import pytest

from code.auth.utils import get_password_hash
from code.models import User


@pytest.fixture
async def user() -> User:
    return await User.create(username='username', password_hash=get_password_hash('password'))
