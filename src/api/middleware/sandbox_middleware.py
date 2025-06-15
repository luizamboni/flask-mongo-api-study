from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SandboxContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_sandbox = request.headers.get("x-sandbox-request") == "true"
        config = request.app.state.config

        if is_sandbox:
            print("it is sandbox!")
            request.app.state.ticket_service = config.sandbox.ticket_service
            request.app.state.health_service = config.sandbox.health_service
        else:
            print("it is regular!")
            request.app.state.ticket_service = config.regular.ticket_service
            request.app.state.health_service = config.regular.health_service

        response = await call_next(request)
        return response
