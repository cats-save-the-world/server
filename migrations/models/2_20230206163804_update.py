from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "skins" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "type" VARCHAR(6) NOT NULL,
    "name" VARCHAR(40) NOT NULL,
    "price" INT NOT NULL
);
COMMENT ON COLUMN "skins"."type" IS 'CAT: cat\nPLANET: planet';;
        CREATE TABLE IF NOT EXISTS "user_skins" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "skin_id" UUID NOT NULL REFERENCES "skins" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_skins";
        DROP TABLE IF EXISTS "skins";
        """
