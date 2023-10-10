""" Connection to DataBase of Carrot OCR project"""
import json
from typing import Optional

import psycopg2


class DatabaseManager:
    """Database Manager for Carrot OCR project"""

    def __init__(self, **kwargs):
        """ Initialize the DatabaseManager """
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.database = kwargs.get("database")
        self.table_name = "processed"
        self.connection = None

    def connect(self):
        """
        Connect to the PostgreSQL database.

        :return: True if connection is successful, False otherwise.
        """
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return True
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            return False

    def execute_query(self, query, data=None, fetch=False):
        """
        Execute a SQL query.

        :param data: additional data for query
        :param query: The SQL query to execute.
        :return: True if the query is successful, False otherwise.
        """
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    if data:
                        cursor.execute(query, data)
                    else:
                        cursor.execute(query)
                    self.connection.commit()
                    if fetch:
                        return cursor.fetchall()
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
                new_filename TEXT,
                tags TEXT[],
                text TEXT[],
                bboxes TEXT --in json string
            );
        """
        return self.execute_query(create_table_query)

    @staticmethod
    def from_db(raw: Optional[tuple]) -> Optional[dict]:
        """Convert data from db to template"""
        if len(raw) == 0:
            return None

        data = {
            "id": raw[0],
            "file_path": raw[1],
            "new_filename": raw[2],
            "tags": raw[3],
            "text": raw[4],
            "bboxes": json.loads(raw[5])
        }
        return data

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()