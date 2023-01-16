from asyncio import create_task, sleep
from uuid import UUID

from fastapi import Depends, WebSocket, WebSocketDisconnect

from code.auth.dependencies import get_user
from code.auth.exceptions import InvalidCredentials
from code.auth.utils import get_user_by_credentials
from code.game.consts import EventType
from code.game.controllers import GameController
from code.models import Game, User


async def game_create_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    game = await Game.create(user=user)
    return {'game_id': game.id}


class GameEventsHandler:
    SEND_INTERVAL = 0.1

    async def _authorize(self) -> User:
        data = await self._websocket.receive_json()

        if data.get('type') != EventType.AUTH:
            raise InvalidCredentials

        payload = data['payload']
        return await get_user_by_credentials(payload['username'], payload['password'])

    async def _active_game_exists(self, game_id: UUID, user: User) -> bool:
        return await Game.filter(id=game_id, user=user, is_active=True).exists()

    async def _send_state(self) -> None:
        while True:
            game_state = self._game_controller.state

            if not game_state:
                await self._websocket.send_json(
                    {'type': EventType.GAME_END}
                )
            else:
                await self._websocket.send_json({
                    'type': EventType.STATE,
                    'payload': self._game_controller.state,
                })
            await sleep(self.SEND_INTERVAL)

    async def _receive(self) -> None:
        data = await self._websocket.receive_json()

        if data.get('type') == EventType.CONTROL:
            self._game_controller.control(data['payload'])

    async def __call__(self, websocket: WebSocket, game_id: UUID):  # type: ignore[no-untyped-def]
        self._websocket = websocket
        self._game_controller = GameController()

        await self._websocket.accept()

        try:
            user = await self._authorize()
        except InvalidCredentials:
            return await self._websocket.close()

        if not await self._active_game_exists(game_id, user):
            return await self._websocket.close()

        task = create_task(self._send_state())

        try:
            while True:
                await self._receive()
        except WebSocketDisconnect:
            self._game_controller.stop_clock()
            task.cancel()
