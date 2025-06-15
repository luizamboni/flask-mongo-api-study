from motor.motor_asyncio import AsyncIOMotorClient

class MongoInitializer:
    instances: dict[str,AsyncIOMotorClient] = {}

    async def get_instance(self, url_connection: str):
        if client := self.instances.get(url_connection):
            return client
    
        client = AsyncIOMotorClient(url_connection)
        self.instances[url_connection] = client
        return client

mongo_initializer = MongoInitializer()

__all__ = ["mongo_initializer"]