FROM python:3.10-slim

ARG POETRY_VERSION=1.4.2

ENV PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml /app/

RUN poetry install

CMD python /app/migrations/main.py && python /app/bin/main.py
