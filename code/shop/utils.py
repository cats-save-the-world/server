from code.models import Skin, User, UserSkin
from code.shop.consts import CAT_DEFAULT_SKIN_NAME


async def get_shop_skins(user: User) -> list[dict] | dict:
    user_skins = await UserSkin.filter(
        user=user,
    ).only(
        'skin_id',
        'is_active',
    )

    skins = await Skin.filter(type=Skin.Type.CAT).values('id', 'name', 'price')
    user_skins = {skin.skin_id: skin.is_active for skin in user_skins}  # type: ignore[attr-defined]

    for skin in skins:
        if skin['id'] in user_skins:
            skin['is_bought'] = True
            skin['is_active'] = user_skins[skin['id']]

        else:
            skin['is_bought'] = False
            skin['is_active'] = False

    return skins


async def get_user_skins(user: User) -> dict:
    cat = await (
        UserSkin.filter(is_active=True, skin__type=Skin.Type.CAT)
        .select_related('skin')
        .first()
        .values(name='skin__name')  # noqa: C812
    )
    return {'cat': cat}


async def create_default_skins(user: User) -> None:
    skin = await Skin.get_or_none(name=CAT_DEFAULT_SKIN_NAME)
    await UserSkin.create(user=user, skin=skin, is_active=True)
