from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from code.auth.utils import password_matches
from code.models import User

security = HTTPBasic()


async def get_user(credentials: HTTPBasicCredentials = Depends(security)) -> Optional[User]:
    user = await User.get_or_none(username=credentials.username)

    if not user or not password_matches(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
