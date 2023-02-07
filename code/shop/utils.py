from tortoise.expressions import Case, When

from code.models import Skin, User, UserSkin


async def get_user_skins(user: User) -> list[dict]:
    user_skins = await UserSkin.filter(
        user=user,
    ).only(
        'skin_id',
        'is_active',
    )

    return await Skin.annotate(
        is_active=Case(
            When(
                id__in=[skin.skin_id for skin in user_skins if skin.is_active is True],
                then=True,
            ),
            default=False,
        ),
        is_bought=Case(
            When(
                id__in=[skin.skin_id for skin in user_skins],
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
