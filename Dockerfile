FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]