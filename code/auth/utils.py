from passlib.context import CryptContext

from code.auth.exceptions import InvalidCredentials
from code.models import User

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)


def password_matches(password: str, password_hash: str) -> bool:
    return crypt_context.verify(password, password_hash)


async def get_user_by_credentials(username: str, password: str) -> User:
    user = await User.get_or_none(username=username)

    if not user or not password_matches(password, user.password_hash):
        raise InvalidCredentials

    return user
