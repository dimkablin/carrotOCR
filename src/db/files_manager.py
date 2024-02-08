"""Processed table manager."""
import json
from typing import Optional, List, Union
from psycopg2 import extensions

from src.db.database_manager import DatabaseManager
from src.db.structures.file_structure import FileStructure
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


class FilesManager:
    """Class to work with Database Manager."""
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }
    table_name = "files"

    @staticmethod
    def create_table():
        """
        Create the 'processed' table.

        :return: True if table creation is successful, False otherwise.
        """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {FilesManager.table_name} (
                id SERIAL PRIMARY KEY,
                chunk_id INTEGER NOT NULL,
                old_filename TEXT,
                new_filename TEXT
            );
        """

        with DatabaseManager(**FilesManager.db_config) as db_manager:
            if db_manager.connect():
                db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                return db_manager.execute_query(create_table_query)
        return None

    @staticmethod
    def insert_data(raw: FileStructure) -> Optional[int]:
        """Insert data into the database."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"""
                INSERT INTO {FilesManager.table_name} (chunk_id, old_filename)
                VALUES (%s, %s)
                RETURNING id
            """
            data = (
                raw.chunk_id,
                raw.old_filename
            )

            return db_manager.execute_query(query, data, fetch=True)[0][0]

    @staticmethod
    def get_data_by_id(uid: int) -> FileStructure:
        """Get data from the database by id."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"SELECT * FROM {FilesManager.table_name} WHERE id = %s"
            data = (uid,)
            result = db_manager.execute_query(query, data, fetch=True)
            return FileStructure().from_db(result[0])

    @staticmethod
    def delete_data_by_id(uid: int) -> bool:
        """Delete data from the database by id."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"DELETE FROM {FilesManager.table_name} WHERE id = %s"
            data = (uid,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def delete_data_by_chunk_id(chunk_id: int) -> bool:
        """ Delete data from the database by chunk_id."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"DELETE FROM {FilesManager.table_name} WHERE chunk_id = %s"
            data = (chunk_id,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def get_data_by_chunk_id(chunk_id: int) -> List[FileStructure]:
        """Get data from the database by chunk_id."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"SELECT * FROM {FilesManager.table_name} WHERE chunk_id = %s"
            data = (chunk_id,)
            result = db_manager.execute_query(query, data, fetch=True)
            return [FileStructure().from_db(i) for i in result]

    @staticmethod
    def insert_new_filename(new_filename: str, uid: int) -> bool:
        """Insert new_filename into the database by given ID."""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"""
                UPDATE {FilesManager.table_name}
                SET new_filename = %s
                WHERE id = %s
            """
            data = (new_filename, uid)
            return db_manager.execute_query(query, data)

    @staticmethod
    def clear_table() -> bool:
        """Clear all data from table"""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"""TRUNCATE TABLE {FilesManager.table_name} RESTART IDENTITY;"""
            return db_manager.execute_query(query)

    @staticmethod
    def get_all_data() -> Optional[tuple]:
        """Get all data from db"""
        with DatabaseManager(**FilesManager.db_config) as db_manager:
            query = f"""SELECT * FROM {FilesManager.table_name}"""
            return db_manager.execute_query(query, fetch=True)
