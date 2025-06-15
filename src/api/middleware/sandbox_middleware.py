
from typing import Awaitable
from starlette.types import Scope, Receive, Send

from src.api.app import AppInterface
from src.initializers.configuration import Configuration
 
class SandboxContextMiddleware:
    def __init__(self, app: AppInterface, config: Configuration):
        self.app = app
        self.config = config

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> Awaitable[None]:

        is_sandbox = False
        if scope["type"] == "http":
            for header_name, value in scope.get("headers", []):
                if header_name == b'x-sandbox-request' and value == b'true':
                    is_sandbox = True
                    break
    
        if is_sandbox:
            print("it is sandbox!")

            scope["app"].state.ticket_service = self.config.sandbox.ticket_service
            scope["app"].state.health_service = self.config.sandbox.health_service
        else:
            print("it is regular!")

            scope["app"].state.ticket_service = self.config.regular.ticket_service
            scope["app"].state.health_service = self.config.regular.health_service

        await self.app(scope, receive, send)