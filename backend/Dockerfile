FROM python:3.11-slim

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

RUN apt-get update && \
    apt-get install -y dos2unix

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev

CMD ["bash", "/app/run_django.sh"]

COPY . /app/

#RUN poetry run python manage.py collectstatic --noinput

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]


RUN poetry install --no-root