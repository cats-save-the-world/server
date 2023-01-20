from pydantic import BaseModel, StrictStr


class UsernameSchema(StrictStr):
    regex = '^[a-zA-Z0-9_.-]{3,20}$'


class PasswordSchema(StrictStr):
    min_length = 8
    max_length = 100
    strip_whitespace = True


class UserCreateSchema(BaseModel):
    username: UsernameSchema
    password: PasswordSchema
