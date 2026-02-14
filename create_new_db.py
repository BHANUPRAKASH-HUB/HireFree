import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Connect to default 'postgres' database to create the new one
    try:
        con = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='localhost',
            password='Charan@123'
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        db_name = 'freelancer_hiring_db'
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database: {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")
            print("Database created successfully!")
        else:
            print(f"Database {db_name} already exists.")
            
        cur.close()
        con.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

if __name__ == '__main__':
    create_database()
