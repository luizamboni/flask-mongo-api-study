from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Any

class TicketEvent(BaseModel):
    name: str
    data: dict[str,Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class Ticket(BaseModel):
    id: str
    reason: str
    created_at: datetime = Field(default_factory=datetime.now)
    events: list[TicketEvent] = Field(default_factory=list)

    def add_event(self, name: str, data: dict):
        self.events.append(
            TicketEvent(
                name=name,
                data=data,
            )
        )
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')})

class CreateTicket(BaseModel):
    id: str
    reason: str

__all__ = ("Ticket", "CreateTicket",)