from fastapi import Depends

from code.auth.dependencies import get_user
from code.models import User
from code.shop.utils import get_shop_skins


async def get_skins(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    return await get_shop_skins(user)
