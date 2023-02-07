from uuid import UUID

from pydantic import BaseModel


class SkinSchema(BaseModel):
    id: UUID  # noqa: A003
    name: str
    price: int
    is_bought: bool
    is_active: bool
