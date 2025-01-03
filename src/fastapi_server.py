from fastapi import FastAPI
import yaml
from yaml import Loader

from .initializers.mongo import mongo_initializer 
from .domain.service import TicketService, CreateTicket
from .api.ticket import TicketEventSchema, TicketSchema, CreateTicketSchema
app = FastAPI()


config = {}
with open("src/configs/development.yml") as f:
    raw_config = f.read()
    config = yaml.load(raw_config, Loader=Loader)


ticket_service = TicketService(
    connection = mongo_initializer.get_instance(url_connection=config["mongo"]["url"])
)

@app.get("/health")
async def health():
    mongo_client = await mongo_initializer.get_instance(url_connection=config["mongo"]["url"])
    try:
        resp = await mongo_client.admin.command('ping')
        return {}
    except Exception as e:
        return {
            "err": str(e)
        }

@app.get("/ticket/", response_model=list[TicketSchema])
async def get_tickets():
    tickets = await ticket_service.find_many()
    return [ TicketSchema(**ticket.model_dump()) for ticket in tickets] 

@app.post("/ticket", response_model=TicketSchema)
async def create_ticket(body_scheme: CreateTicketSchema):
    ticket = await ticket_service.create_one(
        payload=CreateTicket(**body_scheme.model_dump())
    )
    return TicketSchema(**ticket.model_dump())

@app.get("/ticket/{id}", response_model=TicketSchema)
async def get_ticket(id: str):
    ticket = await ticket_service.find_one(id=id)
    if ticket:
        return ticket.model_dump()
    return {}, 404


@app.post("/ticket/{id}/event", response_model=TicketSchema)
async def get_ticket(id: str, body_scheme: TicketEventSchema):
   

    ticket = await ticket_service.add_event(
        id=id, 
        name=body_scheme.name,
        data=body_scheme.data
    )
    return TicketSchema(**ticket.model_dump())

