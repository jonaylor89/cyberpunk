###############################################
# Base Image
###############################################
FROM python:3.9-slim as python-base

ENV PYTHONUNBUFFERED=1  \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off  \
    PIP_DISABLE_PIP_VERSION_CHECK=on  \
    PIP_DEFAULT_TIMEOUT=100  \
    POETRY_VERSION=1.0.5  \
    POETRY_HOME="/opt/poetry"  \
    POETRY_VIRTUALENVS_IN_PROJECT=true  \
    POETRY_NO_INTERACTION=1  \
    PYSETUP_PATH="/opt/pysetup"  \
    VENV_PATH="/venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

RUN apt-get update  \
    && apt-get install --no-install-recommends -y  \
    curl  \
    build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN python -m venv $VENV_PATH

COPY pyproject.toml poetry.lock ./

RUN . /venv/bin/activate && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

COPY . .

RUN . /venv/bin/activate && poetry build

###############################################
# Production Image
###############################################
FROM python-base as production

RUN apt-get update  \
    && apt-get install --no-install-recommends -y  \
    ffmpeg

COPY --from=builder-base /venv /venv
COPY --from=builder-base /opt/pysetup/dist .
RUN . /venv/bin/activate && pip install *.whl

COPY main.py .
COPY cyberpunk.yaml .

# COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

EXPOSE $PORT
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
