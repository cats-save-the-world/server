from uuid import UUID

from fastapi import Depends, HTTPException, status
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from code.auth.dependencies import get_user
from code.models import Skin, Transaction, User, UserSkin
from code.shop.utils import get_shop_skins


async def get_skins_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    return await get_shop_skins(user)


async def buy_skin_handler(  # type: ignore[no-untyped-def]
    skin_id: UUID, user: User = Depends(get_user),
):
    skin = await Skin.get_or_none(id=skin_id)

    if skin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user.balance < skin.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        async with in_transaction():
            user_skin, created = await UserSkin.get_or_create(user=user, skin=skin)

            if not created:
                user.balance -= skin.price
                await user.save(update_fields=['balance'])
                await Transaction.create(
                    user=user, reference_id=user_skin, amount=skin.price,
                    type=Transaction.Type.SKIN_PURCHASE,
                )
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
