from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class TicketEventSchema(BaseModel):
    name: str
    data: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)

class TicketSchema(BaseModel):
    id: str
    reason: str
    events: list[TicketEventSchema] = Field(default_factory=[])

class CreateTicketSchema(BaseModel):
    id: str
    reason: str

class TicketCancellationSchema(BaseModel):
    reason: str
