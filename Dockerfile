FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y default-jdk maven
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2==2.9.6

COPY requirements.txt /app/
COPY /scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5432
EXPOSE 5433



