from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "transactions" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "type" VARCHAR(13) NOT NULL,
    "reference_id" UUID NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" INT NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "transactions"."type" IS 'SKIN_PURCHASE: skin_purchase';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "transactions";"""
