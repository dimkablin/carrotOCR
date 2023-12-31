# pylint: disable=R,E
"""permatags table manager"""
from typing import Optional
from psycopg2 import extensions
from src.api.models.tags import GetPermatagsResponse, PermatagsResponse

from src.db.database_manager import DatabaseManager
from src.db.structures.permatags_structure import PermatagsStructure
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

class PermatagsManager:
    """Class to work with Database Manager."""
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }
    table_name = "permatags"

    @staticmethod
    def create_table():
        """
        Create the 'permatags' table.

        :return: True if table creation is successful, False otherwise.
        """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {PermatagsManager.table_name} (
                id SERIAL PRIMARY KEY,
                group_id INTEGER NOT NULL,
                tag TEXT NOT NULL
            );
        """

        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            if db_manager.connect():
                db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                return db_manager.execute_query(create_table_query)
        return None

    @staticmethod
    def insert_data(raw: PermatagsStructure) -> Optional[int]:
        """Insert data into the database."""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            check_query = f"SELECT * FROM {PermatagsManager.table_name} \
                WHERE tag = %s AND group_id = %s"
            check_data = (raw.tag, raw.group_id)
            #Если не нашли в бд тэг
            if not db_manager.execute_query(check_query, check_data, fetch=True):
                query = f"""
                    INSERT INTO {PermatagsManager.table_name} (group_id, tag)
                    VALUES (%s, %s)
                    RETURNING id
                """
                data = (raw.group_id, raw.tag)
                return db_manager.execute_query(query, data, fetch=True)[0][0]

    @staticmethod
    def get_data_by_id(uid: int) -> PermatagsStructure:
        """Get data from the database by id."""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"SELECT * FROM {PermatagsManager.table_name} WHERE id = %s"
            data = (uid,)
            result = db_manager.execute_query(query, data, fetch=True)
            return PermatagsStructure().from_db(result[0])

    @staticmethod
    def delete_data_by_id(uid: int) -> bool:
        """Delete data from the database by id."""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"DELETE FROM {PermatagsManager.table_name} WHERE id = %s"
            data = (uid,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def delete_data_by_tag(tag: str, group_id: int) -> bool:
        """Delete data from the database by id."""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"DELETE FROM {PermatagsManager.table_name} WHERE tag = %s AND group_id=%s"
            data = (tag,group_id,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def clear_table() -> bool:
        """Clear all data from table"""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"""TRUNCATE TABLE {PermatagsManager.table_name} RESTART IDENTITY;"""
            return db_manager.execute_query(query)

    @staticmethod
    def convert_raw_tags(result: list) -> GetPermatagsResponse:
        """Convert query detch result to GetPermatagsResponse"""
        result = [
                PermatagsResponse(
                    uid=i[0],
                    group_id=i[1],
                    tag=i[2]
                )
                for i in result
            ]
        return GetPermatagsResponse(tags=result)

    @staticmethod
    def get_data_by_group(group_id: int) -> Optional[tuple]:
        """Get all data from db"""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"""SELECT * FROM {PermatagsManager.table_name} WHERE group_id=%s"""
            data=(group_id,)
            result = db_manager.execute_query(query, data, fetch=True)

            return PermatagsManager.convert_raw_tags(result)

    @staticmethod
    def get_all_data() -> Optional[tuple]:
        """Get all data from db"""
        with DatabaseManager(**PermatagsManager.db_config) as db_manager:
            query = f"""SELECT * FROM {PermatagsManager.table_name}"""
            result = db_manager.execute_query(query, fetch=True)

            return PermatagsManager.convert_raw_tags(result)
