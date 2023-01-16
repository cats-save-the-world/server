from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from code.auth.exceptions import InvalidCredentials
from code.auth.utils import get_user_by_credentials
from code.models import User

security = HTTPBasic()


async def get_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    try:
        user = await get_user_by_credentials(credentials.username, credentials.password)
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
