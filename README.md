TatneftIT 
==============================

Implementation of OCR from open sources for internal tasks of the Tatneft Group.

Project Organization
------------

    ├── LICENSE
    ├── Makefile                <- Makefile with commands like `make data` or `make train`
    ├── README.md               <- The top-level README for developers using this project.
    │
    ├── docs                    <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                  <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks               <- Jupyter notebooks. Example of the model usage.
    │
    ├── requirements.txt 
    │
    ├── setup.py                <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                     <- Source code for use in this project.
    │   ├── api                 
    │   │   ├── services        <- Fast API services.
    │   │   ├── models          <- Fast API models.
    │   │   └── main.py
    │   │
    │   ├── db                  <- Scripts that using for connect to the database.
    │   │   ├── database_manager.py
    │   │   └── database_processor.py
    │   │
    │   │
    │   ├── features            <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models              <- Scripts with loading trained models.
    │   │   ├── ocr.py
    │   │   └── zero_shot_classification.py
    │   │
    │   └── visualization       <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests                   <- Unittest for each class in src. 
    │   └── ...
    │
    └── tox.ini                 <- tox file with settings for running tox; see tox.readthedocs.io


--------
## PostgreSQL Setup
**_NOTE_**: A pre-existing database is required in order to create a connection to PostgreSQL.
```bash
sudo -u postgres psql
```
Once you're connected to PostgreSQL, you can create a new database and grant privileges to a user using the following SQL statements:
```bash
CREATE DATABASE database_name;
CREATE USER user_name with encrypted password 'user_password';
GRANT ALL PRIVILEGES ON DATABSE database_name TO user_name;
```
Ensure that `database_name`, `user_name`, `user_password` with the appropriate values, which should also be defined in your .env file.


After creating the database and user, you can run a script that will create the necessary databases and tables for the project:
```bash
# Run the script that create database and tables
python3 db_script.py
```

## Run project
It is preferable to run the project on the linux
```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```
where you can choose --host and --port 

## Example of usage

```python
import mmcv
from src.visualization.visualize import *
from src.models.ocr import OCRModelFactory

url = 'data/raw/example1.jpg'
image = mmcv.imread(url)

model = OCRModelFactory.create("pytesseract")
outputs = model([image])
result2show(image, outputs[0])
```

<img src="notebooks/references/output1.png" alt="#">