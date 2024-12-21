from pydantic import BaseModel

class Ticket(BaseModel):
    id: str
    reason: str
    