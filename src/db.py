import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'tracker')
        )
        return conn
    except mysql.connector.Error as e:
        print(f"✗ Database connection failed: {e}")
        raise SystemExit(1)
