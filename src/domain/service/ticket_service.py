from .model.ticket import Ticket

class TicketService:

    def __init__(self, connection):
        self.connection = connection
        self.connection_resolved = None
    
    async def _get_collection(self):
        if not self.connection_resolved:
            self.connection_resolved = await self.connection
        db = self.connection_resolved["poc_database"]
        return db.get_collection("tickets")
    
    async def find_many(self):
        collection = await self._get_collection()
        docs = await collection.find().to_list()
        return [ Ticket(**doc) for doc in docs]
    
    async def find_one(self, id: str):
        collection = await self._get_collection()
        doc = await collection.find_one({"id": id})
        if doc:
            return Ticket(**doc)
        return None

    async def create_one(self, id: str, payload: dict = dict()):
        collection = await self._get_collection()
        doc = await collection.find_one_and_replace(
            filter={"id": id}, 
            replacement=payload, 
            upsert=True # will create a new document if not exists
        )
    
        return Ticket(**doc)


__all__ = ("TicketService",)