from fastapi import Depends

from code.auth.dependencies import get_user
from code.models import User
from code.shop.utils import get_user_skins


async def get_skins(user: User = Depends(get_user)) -> list[dict]:  # type: ignore[no-untyped-def]
    skins = await get_user_skins(user)
    return skins
