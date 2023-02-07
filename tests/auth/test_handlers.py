from fastapi import status
from httpx import AsyncClient

from code.models import Skin, User, UserSkin


async def test_user_create_handler(client: AsyncClient, default_cat_skin: Skin) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = await User.first()
    user_default_skin = UserSkin.filter(user=user, skin=default_cat_skin, is_active=True)
    assert user and user.username == 'username'
    assert await user_default_skin.exists() is True


async def test_user_create_handler__already_exists(client: AsyncClient, user: User) -> None:
    response = await client.post(
        '/auth/users', json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_verify_handler(client: AsyncClient, user: User) -> None:
    response = await client.get('/auth/verify', auth=('username', 'password'))
    assert response.status_code == status.HTTP_200_OK


async def test_verify_handler__user_not_found(client: AsyncClient) -> None:
    response = await client.get('/auth/verify', auth=('username', 'password'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_username_exists_handler__exists(client: AsyncClient, user: User) -> None:
    response = await client.get('/auth/users', params={'username': 'username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


async def test_username_exists_handler(client: AsyncClient) -> None:
    response = await client.get('/auth/users', params={'username': 'username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is False
