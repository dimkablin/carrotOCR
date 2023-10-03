""" Connection to DataBase of Carrot OCR project"""
import psycopg2


def create_db_connection():
    """ Creating database function """
    try:
        connection = psycopg2.connect(
            user="dimka",
            password="admin",
            host="localhost",
            port="5432",
            database="carrot_ocr"
        )

        return connection
    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL", error)
        return None
