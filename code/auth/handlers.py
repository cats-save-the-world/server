from fastapi import HTTPException, Response, status
from tortoise.exceptions import IntegrityError

from code.auth.schemas import UserCreateSchema
from code.auth.utils import get_password_hash
from code.models import User


async def user_create_handler(data: UserCreateSchema):  # type: ignore[no-untyped-def]
    password_hash = get_password_hash(data.password)

    try:
        await User.create(username=data.username, password_hash=password_hash)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return Response(status_code=status.HTTP_201_CREATED)
