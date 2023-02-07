from enum import StrEnum

from tortoise import fields
from tortoise.models import Model


class Skin(Model):
    class Type(StrEnum):
        CAT = 'cat'
        PLANET = 'planet'

    id = fields.UUIDField(pk=True)  # noqa: A003
    type = fields.CharEnumField(Type)  # noqa: A003
    name = fields.CharField(max_length=40)
    price = fields.IntField()

    class Meta:
        table = 'skins'
