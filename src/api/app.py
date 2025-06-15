from typing import Protocol
from src.domain.service.health_service import HealthService
from src.domain.service.ticket_service import TicketService
from starlette.types import ASGIApp


class AppState:
    ticket_service: TicketService
    health_service:  HealthService

class AppInterface(Protocol, ASGIApp):
    state: AppState
    def add_middleware(cb: callable):
        ...