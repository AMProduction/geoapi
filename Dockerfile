# syntax=docker/dockerfile:1
FROM python:3.10.13-slim-bullseye
LABEL authors="andrii_malchyk"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /geoapi

# Install app dependencies
COPY ./requirements.txt /geoapi/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

# Bundle app source
COPY ./geoapi/ /geoapi/

ARG DB_CONNECTION_STRING
ARG DB_SCHEMA_NAME
ARG DB_TABLE_NAME

ENV DB_CONNECTION_STRING=${DB_CONNECTION_STRING}
ENV DB_SCHEMA_NAME=${DB_SCHEMA_NAME}
ENV DB_TABLE_NAME=${DB_TABLE_NAME}

# Creates a non-root user and adds permission to access the /geoapi folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /geoapi
USER appuser


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]