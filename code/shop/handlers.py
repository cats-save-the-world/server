from uuid import UUID

from fastapi import Depends, HTTPException, Response, status
from tortoise.exceptions import OperationalError
from tortoise.expressions import F
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

            if created:
                user.balance = F('balance') - skin.price
                await user.save(update_fields=['balance'])
                await Transaction.create(
                    user=user, reference_id=skin.id, amount=skin.price,
                    type=Transaction.Type.SKIN_PURCHASE,
                )
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)


async def select_skin_handler(  # type: ignore[no-untyped-def]
    skin_id: UUID, user: User = Depends(get_user),
):
    user_skin = await UserSkin.get_or_none(skin_id=skin_id)

    if user_skin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        async with in_transaction():
            await UserSkin.filter(user=user).update(is_active=False)
            user_skin.is_active = True
            await user_skin.save(update_fields=['is_active'])
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)
