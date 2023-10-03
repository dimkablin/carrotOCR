""" Data Base of carrot OCR project Initialization """
from src.db import create_db_connection


def create_database_and_tables():
    """ Init function """
    connection = create_db_connection()

    if connection:
        pass
