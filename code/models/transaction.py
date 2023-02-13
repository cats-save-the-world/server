from enum import StrEnum

from tortoise import fields
from tortoise.models import Model


class Transaction(Model):
    class Type(StrEnum):
        SKIN_PURCHASE = 'skin_purchase'

    id = fields.UUIDField(pk=True)  # noqa: A003
    user = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.User', related_name='transactions',
    )
    type = fields.CharEnumField(Type)  # noqa: A003
    reference_id = fields.UUIDField()
    created_at = fields.DatetimeField(auto_now_add=True)
    amount = fields.IntField()

    class Meta:
        table = 'transactions'
