from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        INSERT INTO "skins" (id, type, name, price) 
        VALUES 
            ('e22ec6d0-70f4-4720-aff2-1744ac973d76', 'cat', 'Default', 0),
            ('d436fc5c-de0c-4650-b934-dfc585ce8b0f', 'cat', 'Boots', 3000),
            ('4cf68eee-2488-4f15-b8cb-805aaa540e35', 'cat', 'Bella', 6000),
            ('5cebf364-3a09-48b7-8d33-7c63b4197148', 'cat', 'Tiger', 12000),
            ('e3eabea7-fccd-4eea-9b30-176d478e7c67', 'cat', 'Luna', 21000),
            ('79e7b08b-eef6-48a4-9618-45edf8d44480', 'cat', 'Shadow', 33000);
            
        INSERT INTO "user_skins" (is_active, skin_id, user_id)  
        SELECT True, 'e22ec6d0-70f4-4720-aff2-1744ac973d76', id  
        FROM users
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DELETE FROM "user_skins" WHERE skin_id = 'e22ec6d0-70f4-4720-aff2-1744ac973d76';
    
        DELETE FROM "skins" where id in (
            'e22ec6d0-70f4-4720-aff2-1744ac973d76',
            'd436fc5c-de0c-4650-b934-dfc585ce8b0f',
            '4cf68eee-2488-4f15-b8cb-805aaa540e35',
            '5cebf364-3a09-48b7-8d33-7c63b4197148',
            'e3eabea7-fccd-4eea-9b30-176d478e7c67',
            '79e7b08b-eef6-48a4-9618-45edf8d44480'
        )
        """
