""" Connection to DataBase of Carrot OCR project"""
import psycopg2


class DatabaseManager:
    """ Database Manager """
    def __init__(self, user: str, password: str, host: int, port: int):
        """ Init database

        :param user:
        :param password:
        :param host:
        :param port:
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = "CarrotOCR"
        self.table_name = "processed"
        self.connection = None

    def connect(self):
        """ Creating database function """
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )

            return True

        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            return False

    def execute_query(self, query: str) -> bool:
        """ Creating table """
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                return True

            except psycopg2.Error as error:
                print("Error creating table: ", error)

        return False

    def create_database(self) -> bool:
        """ Creating database """
        create_database_query = f"""CREATE DATABASE {self.database}"""

        return self.execute_query(create_database_query)

    def create_table(self) -> bool:
        """ Creating table """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                file_path TEXT,
                new_file_name TEXT,
                string_array TEXT[],
                single_string TEXT
            );
        """

        return self.execute_query(create_table_query)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    db_config = {
        "user": "admin",
        "password": "admin",
        "host": "localhost",
        "port": 5432
    }

    # Connect to the PostgreSQL server
    with DatabaseManager(**db_config) as db_manager:
        if db_manager.connect():
            if db_manager.create_database():
                print(f"Database '{db_manager.database}' created successfully.")
            if db_manager.create_table():
                print(f"Table '{db_manager.table_name}' created successfully.")
