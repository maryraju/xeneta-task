import os

DB = {
    "name": "postgres",
    "user": "postgres",
    "host": os.environ["DIP"],
    "password": "docker"
}
