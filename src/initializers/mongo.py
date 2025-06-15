from motor.motor_asyncio import AsyncIOMotorClient

import logging

class MongoInitializer:
    instances: dict[str,AsyncIOMotorClient] = {}

    async def get_instance(self, url_connection: str) -> AsyncIOMotorClient:
        if client := self.instances.get(url_connection):
            logging.debug(f"[MongoInitializer] Reusing existing client for {url_connection}")
            return client
    
        logging.debug(f"[MongoInitializer] Creating new AsyncIOMotorClient for {url_connection}")
        client = AsyncIOMotorClient(url_connection)
        self.instances[url_connection] = client
        return client

mongo_initializer = MongoInitializer()

__all__ = ["mongo_initializer"]