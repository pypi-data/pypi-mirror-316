from pydantic import BaseModel


class SessionHostFormModel(BaseModel):
    class Config:
        validate_assignment = True


class SessionHostForm(SessionHostFormModel):
    namespace: str = ""
    hostname: str = "localhost"
    port: int = 6379
    decode: bool = False
