import asyncio
from asyncio import create_task, sleep
from uuid import UUID

from fastapi import Depends, Response, status, WebSocket
from fastapi.websockets import WebSocketState

from code.auth.dependencies import get_user
from code.auth.exceptions import InvalidCredentials
from code.auth.utils import get_user_by_credentials
from code.game.consts import EventType
from code.game.controllers import GameController
from code.game.exceptions import GameOver
from code.game.utils import finish_game, get_game, update_game_status
from code.models import Game, User

SEND_INTERVAL = 0.1


async def game_create_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    game = await Game.create(user=user)
    return {'game_id': game.id}


async def guest_game_create_handler():  # type: ignore[no-untyped-def]
    game = await Game.create()
    return {'game_id': game.id}


async def assign_guest_game(  # type: ignore[no-untyped-def]
    game_id: UUID, user: User = Depends(get_user),
):
    game = await Game.get_or_none(id=game_id, user=None, status=Game.Status.FINISHED)

    if not game:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    game.user = user
    await game.save()
    return Response(status_code=status.HTTP_200_OK)


async def _authorize(websocket: WebSocket) -> User:
    data = await websocket.receive_json()

    if data.get('type') != EventType.AUTH:
        raise InvalidCredentials

    payload = data['payload']
    return await get_user_by_credentials(payload['username'], payload['password'])


async def _receive_control_events(websocket: WebSocket, game_controller: GameController) -> None:
    while True:
        data = await websocket.receive_json()

        if data.get('type') == EventType.CONTROL:
            game_controller.control(data['payload'])


async def _send_state(websocket: WebSocket, game_controller: GameController) -> None:
    await websocket.send_json({'type': EventType.STATE, 'payload': game_controller.state})


async def _handle_game_over(
    websocket: WebSocket, game: Game, game_controller: GameController,
) -> None:
    await asyncio.gather(
        websocket.send_json({
            'type': EventType.GAME_OVER,
            'payload': {'score': game_controller.score},
        }),
        finish_game(game, game_controller.score),
    )


async def _handle_leave(game: Game) -> None:
    await finish_game(game)


async def game_events_handler(websocket: WebSocket, game_id: UUID):  # type: ignore[no-untyped-def]
    await websocket.accept()
    game = await get_game(game_id)

    if not game:
        return await websocket.close()

    if game.user:
        try:
            user = await _authorize(websocket)
        except InvalidCredentials:
            return await websocket.close()

        if game.user != user:
            return await websocket.close()

    await update_game_status(game, Game.Status.ACTIVE)
    game_controller = GameController()
    task = create_task(_receive_control_events(websocket, game_controller))

    while True:
        try:
            game_controller.tick()
        except GameOver:
            await _send_state(websocket, game_controller)
            await _handle_game_over(websocket, game, game_controller)
            break

        if websocket.client_state == WebSocketState.DISCONNECTED:
            await _handle_leave(game)
            break

        await _send_state(websocket, game_controller)
        await sleep(SEND_INTERVAL)

    task.cancel()
