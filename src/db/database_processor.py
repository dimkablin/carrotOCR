"""Data Processor Package."""
import json
from typing import Optional, List

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
    def insert_data(
            file_path: str,
            tags: List[str],
            text: List[str],
            bboxes: List[List[int]]
    ) -> Optional[List]:
        """Insert data into the database."""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"""
                    INSERT INTO {db_manager.table_name} (file_path, tags, text, bboxes)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """
                data = (file_path, tags, text, json.dumps(bboxes))
                return db_manager.execute_query(query, data, fetch=True)

        except psycopg2.Error as error:
            print("Error inserting data into the database: ", error)
            return None

    @staticmethod
    def get_data_by_id(uid: int) -> Optional[dict]:
        """Get data from the database by id."""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"SELECT * FROM {db_manager.table_name} WHERE id = %s"
                data = (uid,)
                result = db_manager.execute_query(query, data, fetch=True)
                return db_manager.from_db(result)

        except psycopg2.Error as error:
            print("Error during getting data by id: ", error)
        return None

    @staticmethod
    def insert_new_filename(new_filename: str, uid: int) -> bool:
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

    @staticmethod
    def clear_table() -> bool:
        """Clear all data from table"""
        try:
            with DatabaseManager(**DataProcessor.db_config) as db_manager:
                query = f"""DELETE FROM {db_manager.table_name}"""
                return db_manager.execute_query(query)

        except psycopg2.Error as error:
            print("Error inserting data into the database: ", error)
        return False
