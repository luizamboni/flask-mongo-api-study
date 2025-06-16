from contextlib import asynccontextmanager
from fastapi import HTTPException, status
from src.api.app import WebApplication, AppState
from src.api.middleware.sandbox_middleware import SandboxContextMiddleware
from src.initializers.configurator import Configurator

from src.domain.service import CreateTicket
from src.api.ticket import TicketCancellationSchema, TicketEventSchema, TicketSchema, CreateTicketSchema
from src.api.health import HealthSchema




@asynccontextmanager
async def lifespan(app: WebApplication):
    configurator = Configurator()
    config = await configurator.configure()
    print(config)
    app.state.config = config
    
    yield

app = WebApplication(
    lifespan=lifespan,
)

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
    print("APP", app.state.ticket_service) 
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

@app.post("/ticket/{id}/cancel", response_model=TicketSchema)
async def cancel_ticket(id: str, body_scheme: TicketCancellationSchema):


    ticket_with_cancelation = await app.state.ticket_service.find_one(id=id)
    body_scheme.id = id
    app.state.pubsub_publisher_service.publish_event(body_scheme.model_dump())
    return TicketSchema(**ticket_with_cancelation.model_dump())

