import psycopg2 # type: ignore
from decouple import config # type: ignore

class connection:
    @staticmethod
    def db_connection():
        return psycopg2.connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT')
        )