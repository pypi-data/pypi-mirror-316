from pazer_dataform_python import DataForm, DataSubForm
from pazer_logger_python import Logger
import pymysql
from pazer_database_python.DatabaseHostForm import DatabaseHostForm


class DatabaseClient:
    def __init__(self, host: DatabaseHostForm = DatabaseHostForm()):
        self.__host: DatabaseHostForm = host
        self.__state: bool = False
        self.__client: pymysql.connections.Connection | None = None

    def connect(self) -> bool:
        if self.__state and self.__client:
            return True
        if not self.__host:
            Logger.error("[DatabaseClient] Host configuration is not set.")
            return False
        try:
            self.__client = pymysql.connect(
                host=self.__host.hostname,
                user=self.__host.username,
                password=self.__host.password,
                database=self.__host.database,
                port=self.__host.port,
                charset=self.__host.charset,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.__state = True
            return True
        except pymysql.MySQLError as e:
            Logger.error(f"[DatabaseClient] Connection error -> {e}")
            self.close()
            return False

    def close(self) -> None:
        if self.__client:
            try:
                self.__client.close()
            except pymysql.MySQLError as e:
                Logger.error(f"[DatabaseClient] Error closing connection -> {e}")
            finally:
                self.__client = None
                self.__state = False

    def query(self, query: str, params: list | None = None, commit: bool = False) -> DataForm:
        if not self.connect():
            return DataForm(status=False, message=f"[DatabaseClient] Connection error -> {self.__host}")
        try:
            with self.__client.cursor() as cursor:
                cursor.execute(query, params or ())
                if commit:
                    self.__client.commit()
                results = cursor.fetchall() or []
                return DataForm(
                    status=True,
                    data=DataSubForm(items=results, rows=cursor.rowcount, ids=cursor.lastrowid),
                    execute=True
                )
        except Exception as e:
            Logger.error(f"[DatabaseClient] Query Execution Error -> {e}")
            return DataForm(status=False, message=f"[DatabaseClient] Query Execution Error -> {str(e)}")
        finally:
            self.close()

    def select(self, table: str, columnsList: list, columns: list, params: list, like: bool = False,
               equal: bool = False,
               columnsOrder: list | None = None, paramsOrder: list[int] | None = None, limit: int = 10,
               to: int | None = None) -> DataForm:
        toLimit = f" LIMIT {to}, {limit}" if to is not None else f" LIMIT {limit}"
        logical_operator = "AND" if equal else "OR"
        operator = "LIKE" if like else "="
        where_clause = (
            f"WHERE {' ' + logical_operator + ' '.join([f'`{k}` {operator} %s' for k in columns])}"
            if columns else ""
        )
        order_clause = (" ORDER BY " + ", ".join(
            [f"`{col}` {'DESC' if order in [1, True, "true"] else 'ASC'}" for col, order in
             zip(columnsOrder, paramsOrder)]) if columnsOrder and paramsOrder else "")
        list_columns = "*" if not columnsList else ', '.join(f'`{k}`' for k in columnsList)
        query = f"SELECT {list_columns} FROM {table} {where_clause}{order_clause}{toLimit}"
        params = [f"%{v}%" if like else v for v in params]
        return self.query(query=query, params=params)

    def insert(self, table: str, columns: list, params: list) -> DataForm:
        query = f"INSERT INTO {table} ({', '.join([f'`{k}`' for k in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"
        return self.query(query=query, params=params, commit=True)

    def update(self, table: str, columns: list, params: list, columnsValue: list, paramsValue: list,
               limit: int = 1) -> DataForm:
        query = f"UPDATE {table} SET {', '.join([f'`{k}` = %s' for k in columnsValue])} WHERE ({' AND '.join([f'`{k}` = %s' for k in columns])}) LIMIT {limit}"
        return self.query(
            query=query,
            params=paramsValue + params,
            commit=True)

    def delete(self, table: str, columns: list, params: list, limit: int = 1) -> DataForm:
        sanitized_params = [[v] if not isinstance(v, (list, tuple)) else v for v in params]
        where_clause = ' AND '.join(
            [f'`{col}` IN ({", ".join(["%s"] * len(values))})' for col, values in zip(columns, sanitized_params)])
        query = f"DELETE FROM {table} WHERE {where_clause} LIMIT {limit}"
        px = [item for sublist in sanitized_params for item in sublist]
        return self.query(query=query, params=px, commit=True)
