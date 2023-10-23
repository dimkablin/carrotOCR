FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN apt-get install -y \
        build-essential git python3 python3-pip wget \
        ffmpeg libsm6 libxext6 libxrender1 libglib2.0-0

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]