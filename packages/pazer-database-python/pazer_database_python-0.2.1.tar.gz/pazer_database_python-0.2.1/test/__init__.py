import os
import time

from pazer_logger_python import Logger

from pazer_database_python.Executor import Executor

os.environ["ENV"] = "production"
os.environ["DEBUG"] = "true"
os.environ["LOG_ENABLE"] = "true"
Logger.system("HI")

# SESSION
SESSION_HOST_MAIN_READ: str = "main_read"
SESSION_HOST_MAIN_WRITE: str = "main_write"
SESSION_HOST: dict = {
    SESSION_HOST_MAIN_READ: {
        "hostname": "127.0.0.1",
        "port": 6379,
        "namespace": "test",
        "decode": True,
    },
    SESSION_HOST_MAIN_WRITE: {
        "hostname": "127.0.0.1",
        "port": 6379,
        "namespace": "test",
        "decode": True,
    }
}
# DATABASE
DB_SPACE: str = "PZ"
DB_HOST_MAIN_READ: str = "main_read"
DB_HOST_MAIN_WRITE: str = "main_write"
# DATABASE HOST
DB_HOST: dict = {
    DB_HOST_MAIN_READ: {
        "hostname": "localhost",
        "username": "master",
        "password": "expexp",
        "database": "master",
        "port": 3306,
        "charset": "utf8mb4",
    },
    DB_HOST_MAIN_WRITE: {
        "hostname": "localhost",
        "username": "master",
        "password": "expexp",
        "database": "master",
        "port": 3306,
        "charset": "utf8mb4",
    },
}

# database = DatabaseManager()
# database.loads(DB_HOST)
# session = SessionManager()
# session.loads(SESSION_HOST)
executor = Executor()
executor.loads(databaseConfig=DB_HOST,sessionConfig=SESSION_HOST)


# client = executor.database.client(DB_HOST_MAIN_WRITE)
se = executor.sessionClient(SESSION_HOST_MAIN_READ)

# res = se.insert(key="v1",data={"time": time.time()})
# res = se.insert(key="v2",data={"time": time.time()})
# res = se.insert(key="v3",data={"time": time.time()})
# res = se.insert(key="v4",data={"time": time.time()})
# res = se.insert(key="v5",data={"time": time.time()})
# res = se.insert(key="v6",data={"time": time.time()})
# res = se.insert(key="$$:::v7",data={"time": time.time()})
# print(res.data.__dict__)
# res = se.select(key="v4")
# print("Select",res.data.__dict__)
res = se.delete(key="v6")
print("Delete", res.data.__dict__)
#
# res = client.select(
#     table="PZ_USER",
#     columnsList=[],
#     columns=[],
#     params=[],
#     columnsOrder=["NO","NAME"],
#     paramsOrder=[False,True],
#     to=10,
#     limit=10
# )
# res.data.fetch()
# print(res.data.__dict__)
#
#

