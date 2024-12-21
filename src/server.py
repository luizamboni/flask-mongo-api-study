from flask import Flask
from .initializers.mongo import mongo_initializer 
import yaml
from yaml import Loader
from asgiref.wsgi import WsgiToAsgi

config = {}
with open("src/configs/development.yml") as f:
    raw_config = f.read()
    config = yaml.load(raw_config, Loader=Loader)


app = Flask(__name__)

@app.route("/health")
async def health():
    mongo_client = await mongo_initializer.get_instance(url_connection=config["mongo"]["url"])
    try:
        resp = await mongo_client.admin.command('ping')
        print(resp)
        return {}
    except Exception as e:
        return {
            "err": str(e)
        }

@app.route("/", methods=["POST"])
async def create_ticket():
    return {
        "id": "123"
    }

@app.route("/:id", methods=["GET"])
async def get_ticket():
    return {
        "id": "123"
    }

asgi_app = WsgiToAsgi(app)