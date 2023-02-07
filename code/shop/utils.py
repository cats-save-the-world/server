from tortoise.expressions import Case, When

from code.models import Skin, User, UserSkin
from code.shop.consts import CAT_DEFAULT_SKIN_NAME


async def get_shop_skins(user: User) -> list[dict] | dict:
    user_skins = await UserSkin.filter(
        user=user,
    ).only(
        'skin_id',
        'is_active',
    )

    bought_skin_ids = [
        skin.skin_id for skin in user_skins  # type: ignore[attr-defined]
    ]

    active_skin_ids = [
        skin.skin_id for skin in user_skins if skin.is_active is True  # type: ignore[attr-defined]
    ]

    return await Skin.annotate(
        is_active=Case(
            When(
                id__in=active_skin_ids,
                then=True,
            ),
            default=False,
        ),
        is_bought=Case(
            When(
                id__in=bought_skin_ids,
                then=True,
            ),
            default=False,
        ),
    ).filter(
        type=Skin.Type.CAT,
    ).values(
        'id',
        'name',
        'price',
        'is_active',
        'is_bought',
    )


async def get_user_skins(user: User) -> dict:
    return {
        'cat': await UserSkin.filter(is_active=True, skin__type=Skin.Type.CAT)
                             .select_related('skin')
                             .first()
                             .values(name='skin__name'),
    }


async def create_default_skins(user: User) -> None:
    skin = await Skin.get_or_none(name=CAT_DEFAULT_SKIN_NAME)
    await UserSkin.create(user=user, skin=skin, is_active=True)
