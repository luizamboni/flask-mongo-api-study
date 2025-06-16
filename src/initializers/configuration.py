
from pydantic import BaseModel

from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService


from src.domain.service.pubsub_publisher_service import PubSubPublisherService

class EnvironmentConfiguration(BaseModel):
    health_service: HealthService
    ticket_service: TicketService
    pubsub_publisher_service: PubSubPublisherService
    model_config = {
        "arbitrary_types_allowed": True
    }

class Configuration(BaseModel):
    regular: EnvironmentConfiguration
    sandbox: EnvironmentConfiguration