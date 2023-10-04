""" Script that you can run to set project env """
from psycopg2 import extensions
from src.db.database_manager import DatabaseManager
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


if __name__ == "__main__":
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }

    with DatabaseManager(**db_config) as db_manager:
        if db_manager.connect():
            db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            if db_manager.create_database():
                print(f"Database '{db_manager.database}' created successfully.")
            if db_manager.create_table():
                print(f"Table '{db_manager.table_name}' created successfully.")
