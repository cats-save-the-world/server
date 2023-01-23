from fastapi import APIRouter

from code.game import handlers

router = APIRouter()
router.add_api_route('', handlers.game_create_handler, methods=['post'])
router.add_api_route('/guest', handlers.guest_game_create_handler, methods=['post'])
router.add_api_route('/{game_id}', handlers.assign_guest_game, methods=['patch'])
router.add_api_websocket_route('/{game_id}/events', handlers.GameEventsHandler())
