ARG VERSION=3.12
FROM python:$VERSION

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# Install Java and Maven
RUN apt-get update && apt-get install -y default-jdk maven

# Install PostgreSQL client libraries and psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip
# Is there some reason this is not simply in the requirements.txt file that is installed later???
RUN pip install psycopg2==2.9.6

COPY requirements.txt /app/
COPY /scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
COPY /scripts/load_data.sh /app/load_data.sh
RUN chmod +x /app/load_data.sh

COPY . /app/

RUN pip install -r requirements.txt

WORKDIR /usr/local/lib/python$VERSION/site-packages

COPY pagination.html    /usr/local/lib/python$VERSION/site-packages/bootstrap_pagination/templates/bootstrap_pagination/pagination.html
COPY pager.html         /usr/local/lib/python$VERSION/site-packages/bootstrap_pagination/templates/bootstrap_pagination/pager.html

WORKDIR /app
