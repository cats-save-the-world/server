from asyncio import create_task, sleep
from uuid import UUID

from fastapi import Depends, Response, status, WebSocket, WebSocketDisconnect

from code.auth.dependencies import get_user
from code.auth.exceptions import InvalidCredentials
from code.auth.utils import get_user_by_credentials
from code.game.consts import EventType
from code.game.controllers import GameController
from code.game.utils import get_game, update_game_status
from code.models import Game, User


async def game_create_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    game = await Game.create(user=user)
    return {'game_id': game.id}


async def guest_game_create_handler():  # type: ignore[no-untyped-def]
    game = await Game.create()
    return {'game_id': game.id}


async def assign_guest_game(  # type: ignore[no-untyped-def]
    game_id: UUID, user: User = Depends(get_user),
):
    game = await Game.get_or_none(id=game_id, user=None).select_related('user')

    if not game:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    game.user = user
    await game.save(update_fields=['user'])
    return Response(status_code=status.HTTP_200_OK)


class GameEventsHandler:
    SEND_INTERVAL = 0.1

    async def _authorize(self) -> User:
        data = await self._websocket.receive_json()

        if data.get('type') != EventType.AUTH:
            raise InvalidCredentials

        payload = data['payload']
        return await get_user_by_credentials(payload['username'], payload['password'])

    async def _send_events(self) -> None:
        while not self._game_controller.game_over:
            await self._websocket.send_json({
                'type': EventType.STATE,
                'payload': self._game_controller.state,
            })
            await sleep(self.SEND_INTERVAL)

        await self._websocket.send_json({
            'type': EventType.GAME_OVER,
            'payload': {
                'score': self._game_controller.score
            }
        })
        await update_game_status(self._game, Game.Status.FINISHED)

    async def _receive(self) -> None:
        data = await self._websocket.receive_json()

        if data.get('type') == EventType.CONTROL:
            self._game_controller.control(data['payload'])

    async def __call__(self, websocket: WebSocket, game_id: UUID):  # type: ignore[no-untyped-def]
        self._websocket = websocket
        self._game_controller = GameController()
        self._game = await get_game(game_id)

        await self._websocket.accept()

        if not self._game:
            return await self._websocket.close()

        if self._game.user:
            try:
                user = await self._authorize()
            except InvalidCredentials:
                return await self._websocket.close()

            if self._game.user != user:
                return await self._websocket.close()

        await update_game_status(self._game, Game.Status.ACTIVE)
        task = create_task(self._send_events())

        try:
            while True:
                await self._receive()
        except WebSocketDisconnect:
            self._game_controller.stop_clock()
            task.cancel()
            await update_game_status(self._game, Game.Status.FINISHED)
