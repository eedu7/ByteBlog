FROM python:3.12-bluster as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \ 
    POETRY_VIRTUALSENVS_IN_PROJECTS=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -f $POETRY_CACHE_DIR

FROM python:3.12-slim-bluster as runtime

ENV VIRTUAL_ENV = /app/.venv \
    PATH="/app/.venv/bin:PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

ENTRYPOINT ["python", "main.py"]