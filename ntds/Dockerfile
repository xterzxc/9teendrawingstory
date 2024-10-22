# syntax=docker/dockerfile:1.2
FROM python:3.11.4-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip

COPY ./ntds/requirements.txt /app/
RUN pip install -r requirements.txt

RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env ls -l /etc/secrets/
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env

COPY . /app

WORKDIR /app/ntds

RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env python -c "import os; from dotenv import load_dotenv; load_dotenv('/etc/secrets/.env');"
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env python manage.py makemigrations
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env python manage.py migrate

ENTRYPOINT ["gunicorn", "--chdir", "/app/ntds", "ntds.wsgi:application", "-b", "0.0.0.0:8000"]