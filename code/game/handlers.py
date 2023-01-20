from asyncio import create_task, sleep
from uuid import UUID

from fastapi import Depends, WebSocket, WebSocketDisconnect

from code.auth.dependencies import get_user
from code.auth.exceptions import InvalidCredentials
from code.auth.utils import get_user_by_credentials
from code.game.consts import EventType
from code.game.controllers import GameController
from code.game.exceptions import GameEndException
from code.models import Game, User


async def game_create_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    game = await Game.create(user=user)
    return {'game_id': game.id}


async def guest_game_create_handler():  # type: ignore[no-untyped-def]
    game = await Game.create()
    return {'game_id': game.id}


class GameEventsHandler:
    SEND_INTERVAL = 0.1

    async def _authorize(self) -> User:
        data = await self._websocket.receive_json()

        if data.get('type') != EventType.AUTH:
            raise InvalidCredentials

        payload = data['payload']
        return await get_user_by_credentials(payload['username'], payload['password'])

    async def _get_game(self, game_id: UUID) -> Game | None:
        return await Game.get_or_none(id=game_id, is_active=True).select_related('user')

    async def _send_state(self, game_state: dict) -> None:
        await self._websocket.send_json({
            'type': EventType.STATE,
            'payload': game_state,
        })

    async def _end_game(self) -> None:
        self.game.is_active = False
        await self.game.save()

        await self._websocket.send_json({
            'type': EventType.GAME_END,
        })
        await self._websocket.close()

    async def _process_answer(self) -> None:
        while True:
            try:
                game_state = self._game_controller.state
                await self._send_state(game_state)
            except GameEndException:
                await self._end_game()
                return

            await sleep(self.SEND_INTERVAL)

    async def _receive(self) -> None:
        data = await self._websocket.receive_json()

        if data.get('type') == EventType.CONTROL:
            self._game_controller.control(data['payload'])

    async def __call__(self, websocket: WebSocket, game_id: UUID):  # type: ignore[no-untyped-def]
        self._websocket = websocket
        self._game_controller = GameController()

        await self._websocket.accept()
        self.game = await self._get_game(game_id)

        if not self.game:
            return await self._websocket.close()

        if self.game.user:
            try:
                user = await self._authorize()
            except InvalidCredentials:
                return await self._websocket.close()

            if self.game.user != user:
                return await self._websocket.close()

        task = create_task(self._process_answer())

        try:
            while True:
                await self._receive()
        except WebSocketDisconnect:
            self._game_controller.stop_clock()
            task.cancel()
