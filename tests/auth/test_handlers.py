from fastapi import status
from httpx import AsyncClient

from code.models import User


async def test_user_create_handler_success(client: AsyncClient) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = await User.first()
    assert user and user.username == 'username'


async def test_user_create_handler_failure(client: AsyncClient, user: User) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_verify_handler_success(client: AsyncClient, user: User) -> None:
    response = await client.get('/auth/verify', auth=('username', 'password'))
    assert response.status_code == status.HTTP_200_OK


async def test_verify_handler_failure(client: AsyncClient) -> None:
    response = await client.get('/auth/verify', auth=('username', 'password'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_username_exists_handler_success(client: AsyncClient, user: User) -> None:
    response = await client.get('/auth/users', params={'username': 'username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


async def test_username_exists_handler_failure(client: AsyncClient) -> None:
    response = await client.get('/auth/users', params={'username': 'username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is False
