from pydantic import BaseModel


class SessionHostFormModel(BaseModel):
    class Config:
        validate_assignment = True


class SessionHostForm(SessionHostFormModel):
    hostname: str = "localhost"
    port: int = 6379
    namespace: str = "default"
    decode: bool = False
