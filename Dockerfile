FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y postgresql postgresql-contrib
RUN service postgresql start

RUN apt-get install -y \
    build-essential git python3 python3-pip wget \
    ffmpeg libsm6 libxext6 libxrender1 libglib2.0-0

RUN apt-get install -y libpq-dev
RUN apt install -y uvicorn
RUN apt-get install -y postgresql

# PostgreSQL
RUN echo "CREATE DATABASE carrotocr;" > init.sql
RUN echo "CREATE USER admin WITH PASSWORD 'admin';" >> init.sql
RUN echo "GRANT ALL PRIVILEGES ON DATABASE carrotocr TO admin;" >> init.sql

RUN psql -U postgres -f init.sql
CMD ["python3", "/app/db_script.py"]

# Install torch
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install albumentations==1.3.1
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
