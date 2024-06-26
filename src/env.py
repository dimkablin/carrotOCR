""" Script to load environments variables """

import os
import dotenv

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')

dotenv.load_dotenv(dotenv_path)

# importing environment variables from .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SERVER_PATH = os.getenv("SERVER_PATH")
USE_CUDA = eval(os.getenv("USE_CUDA"))
DATA_PATH = str(os.getenv("DATA_PATH"))

if __name__ == "__main__":
    print(project_dir)
