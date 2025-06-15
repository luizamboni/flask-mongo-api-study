from typing import Awaitable, Protocol
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from src.initializers.configurator import Configurator

from src.domain.service import TicketService, CreateTicket, HealthService
from src.api.ticket import TicketEventSchema, TicketSchema, CreateTicketSchema
from src.api.health import HealthSchema

from starlette.types import ASGIApp, Scope, Receive, Send

config = Configurator().configure()
class AppState:
    ticket_service: TicketService  | None
    health_service:  HealthService | None

class AppInterface(Protocol, ASGIApp):
    state: AppState
    def add_middleware(cb: callable):
        ...

class SandboxContextMiddleware:
    def __init__(self, app: AppInterface):
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> Awaitable[None]:

        is_sandbox = False
        if scope["type"] == "http":
            for header_name, value in scope.get("headers", []):
                if header_name == b'x-sandbox-request' and value == b'true':
                    is_sandbox = True
                    break
    
        if is_sandbox:
            print("it is sandbox!")

            scope["app"].state.ticket_service = config.sandbox.ticket_service
            scope["app"].state.health_service = config.sandbox.health_service
        else:
            print("it is regular!")

            scope["app"].state.ticket_service = config.regular.ticket_service
            scope["app"].state.health_service = config.regular.health_service

        await self.app(scope, receive, send)


app: AppInterface = FastAPI()
app.state = AppState()


class ResourceNotFound(BaseModel):
    resource: str

app.add_middleware(SandboxContextMiddleware)


@app.get("/health", response_model=HealthSchema)
async def health():

    try:
        health = await app.state.health_service.check()
        return HealthSchema(**health.model_dump())
    except Exception as e:
        return {
            "err": str(e)
        }

@app.get("/ticket/", response_model=list[TicketSchema])
async def get_tickets():
    tickets = await app.state.ticket_service.find_many()
    return [ TicketSchema(**ticket.model_dump()) for ticket in tickets] 

@app.post("/ticket", response_model=TicketSchema)
async def create_ticket(body_scheme: CreateTicketSchema):
    ticket = await app.state.ticket_service.create_one(
        payload=CreateTicket(**body_scheme.model_dump())
    )
    return TicketSchema(**ticket.model_dump())

@app.get("/ticket/{id}", response_model=TicketSchema)
async def get_ticket(id: str):
    ticket = await app.state.ticket_service.find_one(id=id)
    if ticket is not None:
        return ticket
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ticket with id '{id}' not found."
    )


@app.post("/ticket/{id}/event", response_model=TicketSchema)
async def add_ticket_event(id: str, body_scheme: TicketEventSchema):
   
    ticket = await app.state.ticket_service.add_event(
        id=id, 
        name=body_scheme.name,
        data=body_scheme.data
    )
    return TicketSchema(**ticket.model_dump())

