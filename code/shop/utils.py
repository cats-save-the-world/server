from code.models import Skin, User, UserSkin
from code.shop.consts import CAT_DEFAULT_SKIN_NAME, SkinStatus


async def get_shop_skins(user: User) -> list[dict]:
    purchased_skins = await UserSkin.filter(user=user).only('skin_id', 'is_active')
    skins: list[dict] = await (  # type: ignore[assignment]
        Skin
        .filter(type=Skin.Type.CAT)
        .values('id', 'name', 'price')  # noqa: C812
    )
    skins_map = {
        skin.skin_id: skin.is_active  # type: ignore[attr-defined]
        for skin in purchased_skins
    }

    for skin in skins:
        skin['status'] = SkinStatus.AVAILABLE

        if skin['id'] in skins_map:
            skin['status'] = SkinStatus.SELECTED if skins_map[skin['id']] else SkinStatus.PURCHASED

    return skins


async def get_user_skins(user: User) -> dict:
    cat = await (
        UserSkin
        .filter(user=user, is_active=True, skin__type=Skin.Type.CAT)
        .select_related('skin')
        .first()
        .values(name='skin__name')  # noqa: C812
    )
    return {'cat': cat['name']}  # type: ignore[call-overload]


async def create_default_skins(user: User) -> None:
    skin = await Skin.get_or_none(name=CAT_DEFAULT_SKIN_NAME)
    await UserSkin.create(user=user, skin=skin, is_active=True)
