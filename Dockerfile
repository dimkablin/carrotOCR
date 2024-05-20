FROM python:3.10.9-slim

WORKDIR /carrotocr

COPY . /carrotocr

RUN mkdir -p /carrotocr/LOCAL_DATA && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        python3 \
        python3-pip \
        wget \
        ffmpeg \
        libsm6 \
        libxext6 \
        libxrender1 \
        libglib2.0-0 \
        libicu-dev \
        libcairo2-dev \
        libtesseract-dev \
        tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

