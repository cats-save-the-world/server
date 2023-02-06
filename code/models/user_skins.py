from tortoise import fields
from tortoise.models import Model


class UserSkin(Model):
    id = fields.IntField(pk=True)  # noqa: A003
    user = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.User', related_name='skins',
    )
    skin = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.Skin', related_name='users',
    )
    price = fields.IntField()
    is_active = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'user_skins'
