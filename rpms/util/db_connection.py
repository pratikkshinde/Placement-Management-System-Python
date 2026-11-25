import os
import mysql.connector

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("RPMS_DB_PASSWORD", "")  # Set your MySQL password here
DB_NAME = "rpms_db"


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
