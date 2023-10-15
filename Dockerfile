FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
        build-essential git python3 python3-pip wget \
        ffmpeg libsm6 libxext6 libxrender1 libglib2.0-0

RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN pip3 install torch==2.0.1 torchvision==0.15.2
RUN pip3 install albumentations==1.3.1
RUN pip3 install openmim==0.3.9 mmengine==0.8.4 pip yapf==0.40.1
RUN mim install mmcv==2.0.1 mmdet==3.1.0

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]