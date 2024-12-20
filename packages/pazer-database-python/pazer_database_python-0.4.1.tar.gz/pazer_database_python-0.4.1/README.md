# pazer_database_python

Pazer Database - Python

## install
```bash
pip install pazer_database_python
```

## Example
```python
from pazer_database_python.Executor import Executor

# Database Host
DB_HOST: dict = {
    "name": {
        "hostname": "localhost",
        "username": "user",
        "password": "password",
        "database": "database",
        "port": 3306,
        "charset": "utf8mb4",
    },
}

# Session(Redis) host
SESSION_HOST: dict = {
    "name": {
        "hostname": "127.0.0.1",
        "port": 6379,
        "namespace": "test",
        "decode": True,
    },
}

# Executor Loads
executor = Executor()
executor.loads(
    databaseConfig=DB_HOST,
    sessionConfig=SESSION_HOST,
)

# get Client
DATABASE_client = executor.databaseClient("name")
SESSION_client = executor.sessionClient("name")
```