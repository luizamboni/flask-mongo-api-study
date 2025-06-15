
from pydantic import BaseModel

from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService


class EnvironmentConfiguration(BaseModel):
    health_service: HealthService
    ticket_service: TicketService
    model_config = {
        "arbitrary_types_allowed": True
    }

class Configuration(BaseModel):
    regular: EnvironmentConfiguration
    sandbox: EnvironmentConfiguration