from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)


def password_matches(password: str, password_hash: str) -> bool:
    return crypt_context.verify(password, password_hash)
