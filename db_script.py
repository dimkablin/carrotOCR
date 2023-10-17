""" Script that you can run to set project env """
from src.db.processed_manager import ProcessedManager


if __name__ == "__main__":
    if ProcessedManager.create_table():
        print(f"Table '{ProcessedManager.table_name}' created successfully.")
