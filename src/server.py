from flask import Flask
from .initializers.mongo import mongo_initializer 
from .domain.service import TicketService
import yaml
from yaml import Loader
from asgiref.wsgi import WsgiToAsgi


config = {}
with open("src/configs/development.yml") as f:
    raw_config = f.read()
    config = yaml.load(raw_config, Loader=Loader)


ticket_service = TicketService(
    connection = mongo_initializer.get_instance(url_connection=config["mongo"]["url"])
)

app = Flask(__name__)

@app.route("/health")
async def health():
    mongo_client = await mongo_initializer.get_instance(url_connection=config["mongo"]["url"])
    try:
        resp = await mongo_client.admin.command('ping')
        return {}
    except Exception as e:
        return {
            "err": str(e)
        }

# test
@app.route("/ticket/", methods=["GET"])
async def get_tickets():
    tickets = await ticket_service.find_many()
    print(tickets)
    return [ ticket.model_dump() for ticket in tickets] 

# tese
@app.route("/ticket", methods=["POST"])
async def create_ticket():
    ticket = await ticket_service.create_one(
        id="123", 
        payload={
            "id": "123",
            "reason": "defective product"
        }
    )
    return ticket.model_dump()

@app.route("/ticket/<id>", methods=["GET"])
async def get_ticket(id):
    ticket = await ticket_service.find_one(id="123")
    if ticket:
        return ticket.model_dump()
    return {}


asgi_app = WsgiToAsgi(app)