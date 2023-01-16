from fastapi import APIRouter

from code.game import handlers

router = APIRouter()
router.add_api_route('/', handlers.game_create_handler, methods=['post'])
router.add_api_websocket_route('/{game_id}/events', handlers.GameEventsHandler())
