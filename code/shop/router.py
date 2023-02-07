from fastapi import APIRouter

from code.shop import handlers
from code.shop.schemas import SkinSchema

router = APIRouter()
router.add_api_route('/skins', handlers.get_skins, response_model=list[SkinSchema])
