import psycopg2
from django.http import HttpResponse

from d05.database import connect


def init(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex00_movies (
                    title VARCHAR(64) UNIQUE NOT NULL,
                    episode_nb INTEGER PRIMARY KEY,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL
                )
            """)
    except psycopg2.Error as error:
        return HttpResponse(str(error), content_type="text/plain; charset=utf-8")
    return HttpResponse("OK", content_type="text/plain; charset=utf-8")
