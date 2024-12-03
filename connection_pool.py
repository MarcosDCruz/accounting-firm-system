import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

database_url = input("Enter the Database URL or leave the value empty to load from .env: ")

if not database_url:
    load_dotenv()
    database_url = os.environ["DATABASE_URL"]

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_url)


# context manager for connection handling
@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)
