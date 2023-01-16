from pydantic import BaseModel, constr


class UserCreateSchema(BaseModel):
    username: constr(min_length=6, max_length=20, strip_whitespace=True, to_lower=True)
    password: constr(min_length=8, max_length=100, strip_whitespace=True)
