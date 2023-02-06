from enum import StrEnum

from tortoise import fields
from tortoise.models import Model


class Skin(Model):
    class Type(StrEnum):
        CAT = 'cat'
        PLANET = 'planet'

    id = fields.UUIDField(pk=True)  # noqa: A003
    type = fields.CharEnumField(Type)  # noqa: A003
    price = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'skins'
