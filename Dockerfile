FROM python:3.8.5-slim

WORKDIR /app
COPY pyproject.toml .

RUN pip install poetry
RUN poetry install --no-dev

COPY . .

WORKDIR /app/src

RUN poetry run ./manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
