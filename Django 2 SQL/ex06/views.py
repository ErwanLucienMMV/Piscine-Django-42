import psycopg2
from django.http import HttpResponse
from django.shortcuts import render

from d05.database import connect
from .forms import MovieForm
from .data import MOVIES


def init(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex06_movies (
                    title VARCHAR(64) UNIQUE NOT NULL,
                    episode_nb INTEGER PRIMARY KEY,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated = now();
                    NEW.created = OLD.created;
                    RETURN NEW;
                END;
                $$ LANGUAGE 'plpgsql';
                DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
                CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                update_changetimestamp_column();
            """)
    except psycopg2.Error as error:
        return HttpResponse(str(error), content_type="text/plain; charset=utf-8")
    return HttpResponse("OK", content_type="text/plain; charset=utf-8")


def populate(request):
    messages = []
    for movie in MOVIES:
        try:
            with connect() as connection, connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ex06_movies
                        (episode_nb, title, director, producer, release_date)
                    VALUES (%(episode_nb)s, %(title)s, %(director)s,
                            %(producer)s, %(release_date)s)
                """, movie)
            messages.append("OK")
        except psycopg2.Error as error:
            messages.append(f"{movie['title']}: {error}")
    return render(request, "ex06/messages.html", {"messages": messages})


def display(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ex06_movies ORDER BY episode_nb")
            rows = cursor.fetchall()
            headers = [column.name for column in cursor.description]
        if rows:
            return render(request, "ex06/table.html", {"headers": headers, "rows": rows})
    except psycopg2.Error:
        pass
    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")


def update(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT title FROM ex06_movies ORDER BY episode_nb")
            titles = [row[0] for row in cursor.fetchall()]
            if not titles:
                return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
            form = MovieForm(request.POST if request.method == "POST" else None, titles=titles)
            if request.method == "POST" and form.is_valid():
                cursor.execute("""
                    UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s
                """, [form.cleaned_data["opening_crawl"], form.cleaned_data["title"]])
    except psycopg2.Error:
        return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
    return render(request, "ex06/form.html", {"form": form})
