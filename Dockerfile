FROM python:3.10.9

WORKDIR /carrotocr
COPY . /carrotocr

RUN mkdir /carrotocr/LOCAL_DATA

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    build-essential git python3 python3-pip wget ffmpeg libsm6 libxext6 libxrender1 libglib2.0-0
    
RUN apt install libicu-dev libicu-dev libcairo2-dev libtesseract-dev tesseract-ocr -y

RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

RUN apt install -y uvicorn

RUN pip3 install -r requirements.txt
