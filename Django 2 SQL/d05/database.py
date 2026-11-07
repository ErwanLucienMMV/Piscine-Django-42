"""Open and close the psycopg2 connections used by the SQL apps."""
from contextlib import contextmanager

import psycopg2
from django.conf import settings


@contextmanager
def connect():
    database = settings.DATABASES["default"]
    connection = psycopg2.connect(
        dbname=database["NAME"], user=database["USER"],
        password=database["PASSWORD"], host=database["HOST"],
        port=database["PORT"], connect_timeout=5,
    )
    try:
        with connection:
            yield connection
    finally:
        connection.close()
