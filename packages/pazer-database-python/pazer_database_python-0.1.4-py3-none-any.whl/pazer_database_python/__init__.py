from pazer_database_python.DatabaseClient import DatabaseClient
from pazer_database_python.DatabaseHostForm import DatabaseHostFormModel, DatabaseHostForm
from pazer_database_python.SessionClient import SessionClient
from pazer_database_python.SessionHostForm import SessionHostFormModel, SessionHostForm


class DatabaseManager(DatabaseHostFormModel):
    __host: dict | None = None

    def host(self, name: str) -> DatabaseHostForm:
        self.__host = self.__host or {}
        return self.__host.setdefault(name, DatabaseHostForm())

    def loads(self, host: dict) -> "DatabaseManager":
        self.__host = {k: DatabaseHostForm(**v) for k, v in host.items()}
        return self

    def client(self, name: str) -> DatabaseClient:
        return DatabaseClient(host=self.host(name))


class SessionManager(SessionHostFormModel):
    __host: dict | None = None

    def host(self, name: str) -> SessionHostForm:
        self.__host = self.__host or {}
        return self.__host.setdefault(name, SessionHostForm())

    def loads(self, host: dict) -> "SessionManager":
        self.__host = {k: SessionHostForm(**v) for k, v in host.items()}
        return self

    def client(self, name: str) -> SessionClient:
        return SessionClient(host=self.host(name))
