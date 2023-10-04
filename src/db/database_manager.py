""" Connection to DataBase of Carrot OCR project"""
import os
import psycopg2
from psycopg2 import extensions


class DatabaseManager:
    """Database Manager for Carrot OCR project"""

    def __init__(self, user=None, password=None):
        """
        Initialize the DatabaseManager.

        :param user: The database user.
        :param password: The database password.
        """
        self.user = user or os.getenv("DB_USER")
        self.password = password or os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.table_name = "processed"
        self.connection = None

    def connect(self):
        """
        Connect to the PostgreSQL database.

        :return: True if connection is successful, False otherwise.
        """
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return True
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            return False

    def execute_query(self, query):
        """
        Execute a SQL query.

        :param query: The SQL query to execute.
        :return: True if the query is successful, False otherwise.
        """
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                self.connection.commit()
                return True
            except psycopg2.Error as error:
                print("Error executing query: ", error)
        return False

    def create_database(self):
        """
        Create the database.

        :return: True if database creation is successful, False otherwise.
        """
        create_database_query = f"CREATE DATABASE {self.database}"
        return self.execute_query(create_database_query)

    def create_table(self):
        """
        Create the 'processed' table.

        :return: True if table creation is successful, False otherwise.
        """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY,
                file_path TEXT,
                new_file_name TEXT,
                string_array TEXT[],
                single_string TEXT
            );
        """
        return self.execute_query(create_table_query)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    with DatabaseManager() as db_manager:
        if db_manager.connect():
            db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            if db_manager.create_database():
                print(f"Database '{db_manager.database}' created successfully.")
            if db_manager.create_table():
                print(f"Table '{db_manager.table_name}' created successfully.")
