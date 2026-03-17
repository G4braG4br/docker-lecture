FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home photition

ENV POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PIP_DEFAULT_TIMEOUT=100

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

RUN pip install pre-commit

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-cache

COPY . .

RUN chown -R photition:photition /app

ENV PATH="/app/.venv/bin:$PATH"

USER photition

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
