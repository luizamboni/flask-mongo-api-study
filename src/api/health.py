from pydantic import BaseModel

class HealthSchema(BaseModel):
    ok: bool
