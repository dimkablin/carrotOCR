# pylint: disable=R,E
"""grouptags table manager"""
from psycopg2 import extensions
from src.api.models.database import GrouptagsResponse

from src.db.database_manager import DatabaseManager
from src.db.structures.grouptags_structure import GrouptagsStructure
from src.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

class GrouptagsManager:
    """Class to work with Database Manager."""
    db_config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME
    }
    table_name = "grouptags"

    @staticmethod
    def create_table():
        """
        Create the 'permatags' table.

        :return: True if table creation is successful, False otherwise.
        """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {GrouptagsManager.table_name} (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """

        init_values = [
            GrouptagsStructure(name="Масштаб"),
            GrouptagsStructure(name="Название")
        ]

        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            if db_manager.connect():
                db_manager.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

                # list of results of queries: [True, False, True]
                result = [db_manager.execute_query(create_table_query)]
                for i in init_values:
                    result.append(GrouptagsManager.insert_data(i))

                # return logical AND
                return all(result)

        return None

    @staticmethod
    def insert_data(raw: GrouptagsStructure) -> bool:
        """Insert data into the database."""
        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            query = f"""
                INSERT INTO {GrouptagsManager.table_name} (name)
                VALUES (%s)
            """
            data = (raw.name,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def get_data_by_id(uid: int) -> GrouptagsStructure:
        """Get data from the database by id."""
        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            query = f"SELECT * FROM {GrouptagsManager.table_name} WHERE id = %s"
            data = (uid,)
            result = db_manager.execute_query(query, data, fetch=True)
            return GrouptagsStructure().from_db(result[0])

    @staticmethod
    def delete_data_by_id(uid: int) -> bool:
        """Delete data from the database by id."""
        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            query = f"DELETE FROM {GrouptagsManager.table_name} WHERE id = %s"
            data = (uid,)
            return db_manager.execute_query(query, data)

    @staticmethod
    def clear_table() -> bool:
        """Clear all data from table"""
        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            query = f"""TRUNCATE TABLE {GrouptagsManager.table_name} RESTART IDENTITY;"""
            return db_manager.execute_query(query)

    @staticmethod
    def get_all_data() -> list[GrouptagsResponse]:
        """Get all data from db"""
        with DatabaseManager(**GrouptagsManager.db_config) as db_manager:
            query = f"""SELECT * FROM {GrouptagsManager.table_name}"""
            data = db_manager.execute_query(query, fetch=True)

            if data is not bool:
                data = [
                    GrouptagsStructure().from_db(raw=i)
                    for i in data
                ]
            return data
