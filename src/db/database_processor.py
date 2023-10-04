"""Data Processor Package."""
from typing import Optional

import psycopg2
from src.db.database_manager import DatabaseManager
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


class DataProcessor:
    """Class to work with Database Manager."""
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }

    @staticmethod
    def insert_data(file_path: str, tags: list, text: list, bboxes: list) -> Optional[int, None]:
        """Insert data into the database."""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"""
                    INSERT INTO {db_manager.table_name} (file_path, tags, text, bboxes)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """
                data = (file_path, tags, text, bboxes)
                return db_manager.execute_query(query, data)

        except psycopg2.Error as error:
            print("Error inserting data into the database: ", error)
            return None

    @staticmethod
    def get_data_by_id(uid: int) -> Optional[tuple, None]:
        """Get data from the database by id."""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"SELECT * FROM {db_manager.table_name} WHERE id = %s"
                data = (uid,)

                with db_manager.connection.cursor() as cursor:
                    if db_manager.execute_query(query, data):
                        return cursor.fetchone()

        except psycopg2.Error as error:
            print("Error inserting data into the database: ", error)
        return None

    @staticmethod
    def insert_new_name_of_file(new_filename: str, uid: int) -> bool:
        """Insert new_filename into the database by given ID."""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"""
                    UPDATE {db_manager.table_name}
                    SET new_filename = %s
                    WHERE id = %s
                """
                data = (new_filename, uid)
                return db_manager.execute_query(query, data)

        except psycopg2.Error as error:
            print("Error inserting data into the database: ", error)
        return False
