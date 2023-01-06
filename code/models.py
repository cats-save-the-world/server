from tortoise import fields, Model


class Game(Model):
    id = fields.UUIDField(pk=True)  # noqa: A003
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'games'
