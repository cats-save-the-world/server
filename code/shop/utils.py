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

    for skin in skins:
        for user_skin in user_skins:
            if skin['id'] == user_skin.skin_id:  # type: ignore[attr-defined]
                skin['is_bought'] = True
                skin['is_active'] = user_skin.is_active
                break

            else:
                skin['is_bought'] = False
                skin['is_active'] = False

    return skins


async def get_user_skins(user: User) -> dict:
    return {
        'cat': await UserSkin.filter(user=user, is_active=True, skin__type=Skin.Type.CAT)
                             .select_related('skin')
                             .first()
                             .values(name='skin__name'),
    }


async def create_default_skins(user: User) -> None:
    skin = await Skin.get_or_none(name=CAT_DEFAULT_SKIN_NAME)
    await UserSkin.create(user=user, skin=skin, is_active=True)
