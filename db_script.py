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
    # for t_manager in t_managers:
    #     query = f"DROP TABLE IF EXISTS {t_manager.table_name};"
    #     with DatabaseManager(**ProcessedManager.db_config) as db_manager:
    #         if db_manager.execute_query(query):
    #             print(f"Table {t_manager.table_name} deleted successfulyy")

    # creating tables
    for t_manager in t_managers:
        # Check if the table already exists
        table_exists_query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{GrouptagsManager.table_name}'
            );
        """
        table_exists = DatabaseManager.execute_query(table_exists_query, fetch=True)

        if table_exists[0][0]:
            print(f"Table '{GrouptagsManager.table_name}' already exists.")
            continue
        
        if t_manager.create_table():
            print(f"Table '{t_manager.table_name}' created successfully.")
        
        print(f"Cannot create the '{t_manager.table_name}' table")
