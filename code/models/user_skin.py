from tortoise import fields
from tortoise.models import Model


class UserSkin(Model):
    user = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.User',
    )
    skin = fields.ForeignKeyField(  # type: ignore[var-annotated]
        'models.Skin',
    )
    is_active = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'user_skins'
