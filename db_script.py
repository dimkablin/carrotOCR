""" Script that you can run to set project env """
from src.db.database_manager import DatabaseManager
from src.db.processed_manager import ProcessedManager
from src.db.permatags_manager import PermatagsManager
from src.db.grouptags_manager import GrouptagsManager
from src.db.files_manager import FilesManager


if __name__ == "__main__":
    t_managers = [
        GrouptagsManager,
        ProcessedManager,
        PermatagsManager,
        FilesManager
    ]

    # deleting tables
    for t_manager in t_managers:
        query = f"DROP TABLE IF EXISTS {t_manager.table_name};"
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            if db_manager.execute_query(query):
                print(f"Table {t_manager.table_name} deleted successfulyy")

    # creating tables
    for t_manager in t_managers:
        if t_manager.create_table():
            print(f"Table '{t_manager.table_name}' created successfully.")
