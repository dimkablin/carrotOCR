FROM python:3.10.9

WORKDIR /carrotocr
COPY . /carrotocr

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    build-essential git python3 python3-pip wget \
    ffmpeg libsm6 libxext6 libxrender1 libglib2.0-0

RUN apt install -y uvicorn

RUN pip3 install -r requirements.txt
