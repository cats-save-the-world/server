from tortoise.expressions import Subquery

from code.models import Skin, User, UserSkin


async def get_user_skins(user: User) -> list[dict]:
    return await Skin.annotate(
        is_active=Subquery(UserSkin.filter(user=user, is_active=True).exists()),
        is_bought=Subquery(UserSkin.filter(user=user).exists()),
    ).filter(
        type=Skin.Type.CAT,
    ).values(
        'id',
        'name',
        'price',
        'is_active',
        'is_bought',
    )
