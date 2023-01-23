import pytest

from fastapi import status
from httpx import AsyncClient

from code.models import User


@pytest.mark.anyio
async def test_user_create_handler_success(client: AsyncClient) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = await User.first()
    assert user and user.username == 'username'


@pytest.mark.anyio
async def test_user_create_handler_failure(client: AsyncClient, user: User) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_409_CONFLICT
