from fastapi import APIRouter

from code.shop import handlers

router = APIRouter()
router.add_api_route('/skins', handlers.get_skins_handler)
router.add_api_route('/skins/{skin_id}/buy', handlers.buy_skin_handler)
