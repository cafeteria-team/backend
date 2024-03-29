FROM python:3.9.9-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gdal-bin python3-gdal python3-dev libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
