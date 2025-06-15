from motor.motor_asyncio import AsyncIOMotorClient

class MongoInitializer:
    client: AsyncIOMotorClient | None = None

    async def get_instance(self, url_connection: str):
        # if self.client:
        #     return self.client

        self.client = AsyncIOMotorClient(url_connection)
        return self.client

mongo_initializer = MongoInitializer()

__all__ = ["mongo_initializer"]