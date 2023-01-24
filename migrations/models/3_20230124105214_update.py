from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "score" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "users" ADD "money" INT NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" DROP COLUMN "score";
        ALTER TABLE "users" DROP COLUMN "money";"""
