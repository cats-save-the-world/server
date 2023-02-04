from fastapi import status
from httpx import AsyncClient

from code.models import Game, User


async def test_game_create_handler__no_auth(client: AsyncClient) -> None:
    response = await client.post('/games')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_game_create_handler(client: AsyncClient, user: User) -> None:
    response = await client.post('/games', auth=('username', 'password'))
    assert response.status_code == status.HTTP_200_OK


async def test_guest_game_create_handler(client: AsyncClient) -> None:
    response = await client.post('/games/guest')
    assert response.status_code == status.HTTP_200_OK


async def test_assign_guest_game__no_auth(client: AsyncClient, new_game: Game) -> None:
    response = await client.patch(f'/games/{new_game.id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_assign_guest_game__new_game(client: AsyncClient, user: User, new_game: Game) -> None:
    response = await client.patch(f'/games/{new_game.id}', auth=('username', 'password'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_assign_guest_game__active_game(
    client: AsyncClient, user: User, active_game: Game,
) -> None:
    response = await client.patch(f'/games/{active_game.id}', auth=('username', 'password'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_assign_guest_game__finished_game_with_user(
    client: AsyncClient, user: User, finished_game_with_user: Game,
) -> None:
    response = await client.patch(
        f'/games/{finished_game_with_user.id}', auth=('username', 'password'),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_assign_guest_game(
    client: AsyncClient, user: User, finished_game: Game,
) -> None:
    response = await client.patch(f'/games/{finished_game.id}', auth=('username', 'password'))
    assert response.status_code == status.HTTP_200_OK
    await finished_game.refresh_from_db()
    assert await finished_game.user == user
