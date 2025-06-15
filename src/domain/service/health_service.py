from .health import Health

class HealthService:
    def __init__(self, connection) -> 'HealthService':
        self.connection = connection
        self.connection_resolved = None

    async def _get_collection(self):
        if not self.connection_resolved:
            self.connection_resolved = await self.connection
        return self.connection_resolved.admin

    async def check(self) -> Health:

        try:
            # Attempt a ping command to check DB health
            await (await self._get_collection()).command("ping")
            return Health(ok=True)
        except Exception as e:
            print(e)
            return Health(ok=False)

__all__ = ("HealthService",)