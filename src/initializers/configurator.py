       
from yaml import Loader
import yaml

from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService
from src.initializers.configuration import Configuration, EnvironmentConfiguration
from src.initializers.mongo import mongo_initializer



import logging

class Configurator:
    def __init__(self, profile_name: str = "development"):
        self.config = {}
        with open(f"src/configs/{profile_name}.yml") as f:
            raw_config = f.read()
            self.config = yaml.load(raw_config, Loader=Loader)
        logging.debug(f"[Configurator] Loaded config for profile: {profile_name}")

    async def configure(self) -> Configuration:
        logging.debug("[Configurator] Starting async configuration")
        production_db_connection = await mongo_initializer.get_instance(url_connection=self.config["mongo"]["url"])
        sandbox_db_connection = await mongo_initializer.get_instance(url_connection=self.config["mongo_sandbox"]["url"])
        logging.debug("[Configurator] Mongo clients initialized, building Configuration object")

        return Configuration(
            regular=EnvironmentConfiguration(
                health_service=HealthService(connection=production_db_connection),
                ticket_service=TicketService(connection=production_db_connection),
            ),
            sandbox=EnvironmentConfiguration(
                health_service=HealthService(connection=sandbox_db_connection),
                ticket_service=TicketService(connection=sandbox_db_connection),
            ),
        )
        