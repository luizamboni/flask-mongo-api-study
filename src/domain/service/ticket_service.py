from typing import Any
from .ticket import Ticket, CreateTicket, TicketEvent

class TicketService:

    def __init__(self, connection) -> 'TicketService':
        self.connection = connection
    
    async def _get_collection(self):
        db = self.connection["poc_database"]
        return db.get_collection("tickets")
    
    async def find_many(self) -> list[Ticket]:
        collection = await self._get_collection()
        docs = await collection.find().to_list()
        return [ Ticket(**doc) for doc in docs]
    
    async def find_one(self, id: str) -> Ticket | None:
        collection = await self._get_collection()
        doc = await collection.find_one({"id": id})
        if doc:
            return Ticket(**doc)
        return None

    async def create_one(self, payload: CreateTicket) -> Ticket:
        collection = await self._get_collection()
        doc = await collection.find_one_and_replace(
            filter={"id": payload.id}, 
            replacement=payload.model_dump(), 
            upsert=True # will create a new document if not exists
        ) 
    
        return Ticket(**doc)
    
    async def add_event(self, id: str, name: str, data: dict[str, Any]) -> Ticket:
        collection = await self._get_collection()
        ticket = await self.find_one(id=id)
        ticket.add_event(name=name, data=data)
        doc = await collection.find_one_and_replace(
            filter={"id": ticket.id}, 
            replacement=ticket.model_dump(), 
            upsert=False # will create a new document if not exists
        ) 
    
        return Ticket(**doc)

__all__ = ("TicketService",)