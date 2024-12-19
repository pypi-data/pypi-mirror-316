from pydantic import BaseModel


class DatabaseHostFormModel(BaseModel):
    class Config:
        validate_assignment = True


class DatabaseHostForm(DatabaseHostFormModel):
    hostname: str = "localhost"
    username: str = ""
    password: str = ""
    database: str = ""
    port: int = 3306
    charset: str = "utf8mb4"
