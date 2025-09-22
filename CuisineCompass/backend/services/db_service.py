# services/db_service.py

import psycopg2
from backend.utils.env import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_pg_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
