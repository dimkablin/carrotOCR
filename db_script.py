import asyncio
""" Script that you can run to set project env """
from src.db.database_manager import DatabaseManager
from src.db.processed_manager import ProcessedManager
from src.db.permatags_manager import PermatagsManager
from src.db.grouptags_manager import GrouptagsManager

if __name__ == "__main__":
    t_managers = [
        GrouptagsManager,
        ProcessedManager,
        PermatagsManager
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

async def check_and_initialize_tables():
    t_managers = [
        GrouptagsManager,
        ProcessedManager,
        PermatagsManager
    ]

    missing_tables = False
    for t_manager in t_managers:
        query = f"SELECT to_regclass('{t_manager.table_name}');"
        with DatabaseManager(**ProcessedManager.db_config) as db_manager:
            result = db_manager.execute_query(query)
            
            # Check if result is not a boolean before subscripting
            if not result or (isinstance(result, list) and not result[0][0]):
                missing_tables = True
                break

    if missing_tables:
        print("Missing tables detected, initializing database...")
        process = await asyncio.create_subprocess_exec('python3', 'db_script.py')
        await process.wait()