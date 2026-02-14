import psycopg2
from urllib.parse import urlparse

# Database Config (Hardcoded to match settings.py for this task)
DB_NAME = "hirefree_db"
DB_USER = "postgres"
DB_PASS = "Charan@123"
DB_HOST = "localhost"
DB_PORT = "5432"

def drop_all_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Dropping all tables...")
            cur.execute("DROP SCHEMA public CASCADE;")
            cur.execute("CREATE SCHEMA public;")
            print("Schema reset complete.")
        conn.close()
    except Exception as e:
        print(f"Error resetting DB: {e}")

if __name__ == "__main__":
    drop_all_tables()
