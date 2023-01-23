from copy import deepcopy

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    debug: bool = False
    database_url: PostgresDsn
    test_database_url: PostgresDsn | None = None


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

TEST_TORTOISE_CONFIG = deepcopy(TORTOISE_CONFIG)
TEST_TORTOISE_CONFIG['connections']['default'] = settings.test_database_url  # type: ignore[index]
