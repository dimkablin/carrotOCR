""" Script to load environments variables """

import os
import dotenv

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')

dotenv.load_dotenv(dotenv_path)

if __name__ == "__main__":
    print(project_dir)
