from fastapi import Depends, HTTPException, Response, status
from tortoise.exceptions import IntegrityError

from code.auth.dependencies import get_user
from code.auth.schemas import UserCreateSchema, UsernameSchema
from code.auth.utils import get_password_hash
from code.models import User
from code.shop.utils import create_default_skins


async def user_create_handler(data: UserCreateSchema):  # type: ignore[no-untyped-def]
    password_hash = get_password_hash(data.password)

    try:
        user = await User.create(username=data.username, password_hash=password_hash)
        await create_default_skins(user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return Response(status_code=status.HTTP_201_CREATED)


async def verify_handler(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    return Response(status_code=status.HTTP_200_OK)


async def username_exists_handler(username: UsernameSchema):  # type: ignore[no-untyped-def]
    return await User.filter(username=username).exists()


async def get_my_info(user: User = Depends(get_user)):  # type: ignore[no-untyped-def]
    return {'balance': user.balance}
