import json
import redis
from pazer_dataform_python import DataForm, DataSubForm
from pazer_logger_python import Logger
from redis import Redis
from pazer_database_python.SessionHostForm import SessionHostForm


class SessionClient:
    def __init__(self, host: SessionHostForm = SessionHostForm()):
        self.__host: SessionHostForm | None = host
        self.__state: bool = False
        self.__client: Redis | None = None

    def connect(self) -> bool:
        if not self.__host:
            Logger.error("[SessionClient] Host configuration is not set.")
            return False
        try:
            self.__client = redis.Redis(
                host=self.__host.hostname,
                port=self.__host.port,
                decode_responses=self.__host.decode
            )
            self.__state = self.__client.ping()
            return self.__state
        except redis.ConnectionError as e:
            Logger.error(f"[SessionClient] Connection error -> {e}")
            self.close()
            return False

    def close(self) -> None:
        if self.__client:
            try:
                self.__client.close()
            except redis.ConnectionError as e:
                Logger.error(f"[SessionClient] Error closing connection -> {e}")
            finally:
                self.__client = None
                self.__state = False

    def _get_key(self, key: str) -> str:
        return f"{self.__host.namespace if self.__host.namespace not in ["", None] else "default"}:{key}"

    def _ensure_connection(self) -> bool:
        return self.__state and self.__client and self.__client.ping() or self.connect()

    @staticmethod
    def _create_response(
            status: bool, message: str, data: dict | bool | int | None = None, execute: bool = False
    ) -> DataForm:
        form = DataForm()
        dataForm = DataSubForm()
        if isinstance(data, (dict, int, bool)):
            dataForm.status = True
            if isinstance(data, int):
                if data == 0:
                    dataForm.status = False
                else:
                    dataForm.count = data
                    dataForm.items = [data]
            elif isinstance(data, dict):
                dataForm.count = 1
                dataForm.items = [data]
            elif isinstance(data, bool):
                dataForm.status = bool(data)
        else:
            dataForm.status = False
        form.status = status
        form.message = message
        form.execute = execute
        form.data = dataForm
        return form

    def _handle_operation(self, operation, tag: str, key: str, *args, **kwargs) -> DataForm:
        if not self._ensure_connection():
            return self._create_response(status=False, message="[SessionClient] Client Error")
        try:
            result = operation(self._get_key(key), *args, **kwargs)
            return self._create_response(status=True, message=f"[SessionClient] Session {tag} Completed",
                                         data=result,
                                         execute=True)
        except Exception as e:
            Logger.error(f"[SessionClient] Query Execution Error -> {str(e)}")
            return self._create_response(status=False, message=f"[SessionClient] Query Execution Error -> {str(e)}")
        finally:
            self.close()

    def select(self, key: str) -> DataForm:
        return self._handle_operation(
            operation=lambda k: json.loads(self.__client.get(k)) if self.__client.get(k) else None,
            tag="select",
            key=key
        )

    def insert(self, key: str, data: dict) -> DataForm:
        return self._handle_operation(
            operation=lambda k, v: self.__client.set(k, json.dumps(v)),
            tag="insert",
            key=key,
            v=data
        )

    def delete(self, key: str) -> DataForm:
        return self._handle_operation(
            operation=lambda k: self.__client.delete(k),
            tag="delete",
            key=key
        )
