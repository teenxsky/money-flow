FROM python:3.13-alpine

# Local project path
ENV LOCAL_PROJECT_PATH='/backend'

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# PIP
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'


RUN apk update && \
    apk add --no-cache \
    build-base \
    gettext \
    libpq-dev \
    wget \
    && apk del build-base


WORKDIR /backend

COPY $LOCAL_PROJECT_PATH/poetry.lock $LOCAL_PROJECT_PATH/pyproject.toml /backend/

RUN python -m pip install --no-cache-dir poetry==$POETRY_VERSION \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

RUN poetry install --no-root
