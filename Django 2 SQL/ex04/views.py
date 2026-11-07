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
                CREATE TABLE IF NOT EXISTS ex04_movies (
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


def populate(request):
    messages = []
    for movie in MOVIES:
        try:
            with connect() as connection, connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ex04_movies
                        (episode_nb, title, director, producer, release_date)
                    VALUES (%(episode_nb)s, %(title)s, %(director)s,
                            %(producer)s, %(release_date)s)
                """, movie)
            messages.append("OK")
        except psycopg2.Error as error:
            messages.append(f"{movie['title']}: {error}")
    return render(request, "ex04/messages.html", {"messages": messages})


def display(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ex04_movies ORDER BY episode_nb")
            rows = cursor.fetchall()
            headers = [column.name for column in cursor.description]
        if rows:
            return render(request, "ex04/table.html", {"headers": headers, "rows": rows})
    except psycopg2.Error:
        pass
    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")


def remove(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT title FROM ex04_movies ORDER BY episode_nb")
            titles = [row[0] for row in cursor.fetchall()]
            if not titles:
                return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
            form = MovieForm(request.POST if request.method == "POST" else None, titles=titles)
            if request.method == "POST" and form.is_valid():
                cursor.execute("DELETE FROM ex04_movies WHERE title = %s", [form.cleaned_data["title"]])
                cursor.execute("SELECT title FROM ex04_movies ORDER BY episode_nb")
                titles = [row[0] for row in cursor.fetchall()]
                if not titles:
                    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
                form = MovieForm(titles=titles)
    except psycopg2.Error:
        return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
    return render(request, "ex04/form.html", {"form": form})
