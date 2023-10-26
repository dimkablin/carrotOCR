""" Script to load environments variables """

import os
import dotenv

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')

dotenv.load_dotenv(dotenv_path)

DB_USER = os.getenv("admin")
DB_PASSWORD = os.getenv("admin")
DB_HOST = os.getenv("localhost")
DB_PORT = os.getenv("5432")
DB_NAME = os.getenv("carrotocr")

if __name__ == "__main__":
    print(project_dir)
