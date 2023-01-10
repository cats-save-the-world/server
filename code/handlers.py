import asyncio
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect

from code.controllers import GameController
from code.models import Game

SEND_INTERVAL = 0.1
RECEIVE_INTERVAL = 0.1


async def game_create_handler():
    game = await Game.create()
    return {'game_id': game.id}


async def _send_state(websocket: WebSocket, controller: GameController):
    while True:
        await websocket.send_json(controller.state)
        await asyncio.sleep(SEND_INTERVAL)


async def game_events_handler(websocket: WebSocket, game_id: UUID):
    await websocket.accept()

    if await Game.get_or_none(id=game_id, is_active=True) is None:
        await websocket.close()
        return

    controller = GameController()
    task = asyncio.create_task(_send_state(websocket, controller))

    try:
        while True:
            data = await websocket.receive_json()
            controller.dispatch(data)
            await asyncio.sleep(RECEIVE_INTERVAL)
    except WebSocketDisconnect:
        task.cancel()