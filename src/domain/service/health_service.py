from .health import Health

class HealthService:
    def __init__(self, connection) -> 'HealthService':
        self.connection = connection

    async def _get_collection(self):
        return self.connection.admin

    async def check(self) -> Health:

        try:
            await (await self._get_collection()).command("ping")
            return Health(ok=True)
        except Exception as e:
            print(e)
            return Health(ok=False)

__all__ = ("HealthService",)