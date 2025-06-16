from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SandboxContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.app.state.is_sandbox = request.headers.get("x-sandbox-request") == "true"
        config = request.app.state.config

        if request.app.state.is_sandbox:
            print("it is sandbox!")
            request.app.state.ticket_service = config.sandbox.ticket_service
            request.app.state.health_service = config.sandbox.health_service
            request.app.state.pubsub_publisher_service = config.sandbox.pubsub_publisher_service
        else:
            print("it is regular!")
            request.app.state.ticket_service = config.regular.ticket_service
            request.app.state.health_service = config.regular.health_service
            request.app.state.pubsub_publisher_service = config.regular.pubsub_publisher_service

        response = await call_next(request)
        return response
