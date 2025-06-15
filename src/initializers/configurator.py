       
from yaml import Loader
import yaml

from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService
from src.initializers.configuration import Configuration, EnvironmentConfiguration
from src.initializers.mongo import mongo_initializer



class Configurator:
    def __init__(self, profile_name: str = "development"):
        self.config = {}
        with open(f"src/configs/{profile_name}.yml") as f:
            raw_config = f.read()
            self.config = yaml.load(raw_config, Loader=Loader)

    def configure(self) -> Configuration:
        production_db_connection = mongo_initializer.get_instance(url_connection=self.config["mongo"]["url"])
        sandbox_db_connection = mongo_initializer.get_instance(url_connection=self.config["mongo_sandbox"]["url"])

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
        