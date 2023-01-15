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
    id = fields.UUIDField(pk=True)  # noqa: A003
    user = fields.ForeignKeyField(
        'models.User', related_name='games', null=True,
    )  # type: ignore[var-annotated]
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'games'
