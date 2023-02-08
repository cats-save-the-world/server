from fastapi import APIRouter

from code.shop import handlers

router = APIRouter()
router.add_api_route('/skins', handlers.get_skins)
