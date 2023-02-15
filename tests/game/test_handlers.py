from uuid import uuid4

from fastapi import status
from httpx import AsyncClient

from code.models import Game, UserSkin


async def test_game_create_handler__no_auth(client: AsyncClient) -> None:
    response = await client.post('/games')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_game_create_handler(client: AsyncClient, default_cat_user_skin: UserSkin) -> None:
    response = await client.post('/games', auth=('username', 'password'))
    assert response.status_code == status.HTTP_200_OK


async def test_game_details_handler(client: AsyncClient, finished_game: Game) -> None:
    response = await client.get(f'/games/{finished_game.id}')
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['score'] == finished_game.score


async def test_game_details_handler__not_found(client: AsyncClient) -> None:
    game_id = str(uuid4())
    response = await client.get(f'/games/{game_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
