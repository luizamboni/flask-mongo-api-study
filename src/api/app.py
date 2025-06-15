from fastapi import FastAPI
from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService
from src.initializers.configuration import Configuration


class AppState:
    ticket_service: TicketService
    health_service: HealthService
    config: Configuration

class WebApplication(FastAPI):
    state: AppState
