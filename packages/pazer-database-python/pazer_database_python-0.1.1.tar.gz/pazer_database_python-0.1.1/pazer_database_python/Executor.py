from pazer_database_python import DatabaseManager, SessionManager, DatabaseClient, SessionClient


class Executor:
    def __init__(self, database: DatabaseManager = DatabaseManager(), session: SessionManager = SessionManager()):
        self.database: DatabaseManager = database
        self.session: SessionManager = session
        self.__database: str | None = None
        self.__types: int | None = None

    def loads(self, databaseConfig: dict, sessionConfig: dict) -> None:
        self.database.loads(databaseConfig)
        self.session.loads(sessionConfig)

    def databaseClient(self, name: str) -> DatabaseClient:
        return self.database.client(name)

    def sessionClient(self, name: str) -> SessionClient:
        return self.session.client(name)
