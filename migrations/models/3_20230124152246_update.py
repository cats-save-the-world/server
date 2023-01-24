from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "finished_at" TIMESTAMPTZ;
        ALTER TABLE "games" ADD "score" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "users" ADD "balance" INT NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" DROP COLUMN "finished_at";
        ALTER TABLE "games" DROP COLUMN "score";
        ALTER TABLE "users" DROP COLUMN "balance";"""
