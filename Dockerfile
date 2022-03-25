FROM python:3.9-alpine

# Don't write bytecode .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# stdout and stderr streams will be unbuffered
ENV PYTHONUNBUFFERED=1

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Postgres/psycopg2 related dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


WORKDIR  /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
