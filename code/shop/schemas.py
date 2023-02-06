from uuid import UUID

from pydantic import BaseModel


class SkinSchema(BaseModel):
    id: UUID
    name: str
    price: int
    is_bought: bool
    is_active: bool
