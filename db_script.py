""" Script that you can run to set project env """
from src.db.processed_manager import ProcessedManager
from src.db.permatags_manager import PermatagsManager

if __name__ == "__main__":
    if ProcessedManager.create_table():
        print(f"Table '{ProcessedManager.table_name}' created successfully.")
    if PermatagsManager.create_table():
        print(f"Table '{PermatagsManager.table_name}' created successfully.")
