from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    debug: bool = False
    database_url: PostgresDsn


settings = Settings()


TORTOISE_CONFIG = {
    'connections': {'default': settings.database_url},
    'apps': {
        'models': {
            'models': ['code.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}
