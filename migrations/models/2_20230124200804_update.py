from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "status" VARCHAR(8) NOT NULL  DEFAULT 'new';
        ALTER TABLE "games" ADD "score" INT;
        ALTER TABLE "games" DROP COLUMN "is_active";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "is_active" BOOL NOT NULL  DEFAULT True;
        ALTER TABLE "games" DROP COLUMN "status";
        ALTER TABLE "games" DROP COLUMN "score";"""
