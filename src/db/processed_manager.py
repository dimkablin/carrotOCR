"""Processed table manager."""
import json
from typing import Optional, List, Union
from psycopg2 import extensions

from src.db.database_manager import DatabaseManager
from src.db.structures.processed_structure import ProcessedStructure
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


class ProcessedManager:
    """Class to work with Database Manager."""
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }
    table_name = "processed"

    @staticmethod
    def create_table():
        """
        Create the 'processed' table.

        :return: True if table creation is successful, False otherwise.
        """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {ProcessedManager.table_name} (
                id SERIAL PRIMARY KEY,
                chunk_id INTEGER NOT NULL,
                angle INTEGER,
                old_filename TEXT,
                new_filename TEXT,
                tags TEXT[],
                text TEXT[],
                bboxes TEXT --in json string
            );
        """

        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            if db_manager.connect():
                db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                return db_manager.execute_query(create_table_query)
        return None

    @staticmethod
    def insert_data(raw: ProcessedStructure) -> Optional[int]:
        """Insert data into the database."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"""
                INSERT INTO {ProcessedManager.table_name} (chunk_id, angle, old_filename, tags, text, bboxes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            data = (
                raw.chunk_id,
                raw.angle,
                raw.old_filename,
                raw.tags,
                raw.text,
                json.dumps(raw.bboxes)
            )

            return db_manager.execute_query(query, data, fetch=True)[0][0]

    @staticmethod
    def get_data_by_id(uid: int) -> ProcessedStructure:
        """Get data from the database by id."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"SELECT * FROM {ProcessedManager.table_name} WHERE id = %s"
            data = (uid,)
            result = db_manager.execute_query(query, data, fetch=True)
            return ProcessedStructure().from_db(result[0])

    @staticmethod
    def delete_data_by_id(uid: int) -> bool:
        """Delete data from the database by id."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"DELETE FROM {ProcessedManager.table_name} WHERE id = %s"
            data = (uid,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def delete_data_by_chunk_id(chunk_id: int) -> bool:
        """ Delete data from the database by chunk_id."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"DELETE FROM {ProcessedManager.table_name} WHERE chunk_id = %s"
            data = (chunk_id,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def get_data_by_chunk_id(chunk_id: int) -> ProcessedStructure:
        """Get data from the database by chunk_id."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"SELECT * FROM {ProcessedManager.table_name} WHERE chunk_id = %s"
            data = (chunk_id,)
            result = db_manager.execute_query(query, data, fetch=True)
            return result

    @staticmethod
    def insert_new_filename(new_filename: str, uid: int) -> bool:
        """Insert new_filename into the database by given ID."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"""
                UPDATE {ProcessedManager.table_name}
                SET new_filename = %s
                WHERE id = %s
            """
            data = (new_filename, uid)
            return db_manager.execute_query(query, data)

    @staticmethod
    def clear_table() -> bool:
        """Clear all data from table"""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"""TRUNCATE TABLE {ProcessedManager.table_name} RESTART IDENTITY;"""
            return db_manager.execute_query(query)

    @staticmethod
    def get_text(uid=None) -> Union[str, List[str], None]:
        """Get text by uid, if uid=-1 return all text."""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            if uid is None:
                query = f"""SELECT text FROM {ProcessedManager.table_name}"""
            else:
                query = f"""SELECT text FROM {ProcessedManager.table_name} WHERE id=%s"""
            return db_manager.execute_query(query, (uid,), fetch=True)

    @staticmethod
    def get_all_data() -> Optional[tuple]:
        """Get all data from db"""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"""SELECT * FROM {ProcessedManager.table_name}"""
            return db_manager.execute_query(query, fetch=True)

    @staticmethod
    def update_data_by_id(raw: ProcessedStructure, uid: int) -> bool:
        """Updating data by id"""
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            query = f"""
                UPDATE {ProcessedManager.table_name}
                SET angle=%s, tags = %s, text = %s, bboxes = %s
                WHERE id = %s
            """
            data = (raw.angle, raw.tags, raw.text, json.dumps(raw.bboxes), uid)
            return db_manager.execute_query(query, data)
