from enum import StrEnum

from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.UUIDField(pk=True)  # noqa: A003
    username = fields.CharField(max_length=20, unique=True)
    password_hash = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'users'


class Game(Model):
    class Status(StrEnum):
        NEW = 'new'
        ACTIVE = 'active'
        FINISHED = 'finished'

    id = fields.UUIDField(pk=True)  # noqa: A003
    user = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.User', related_name='games', null=True,
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.CharEnumField(Status, default=Status.NEW)
    score: int | None = fields.IntField(null=True)

    class Meta:
        table = 'games'
