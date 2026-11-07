from pathlib import Path

import psycopg2
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from d05.database import connect


def init(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex08_planets (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    climate VARCHAR,
                    diameter INTEGER,
                    orbital_period INTEGER,
                    population BIGINT,
                    rotation_period INTEGER,
                    surface_water REAL,
                    terrain VARCHAR(128)
                );
                CREATE TABLE IF NOT EXISTS ex08_people (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    birth_year VARCHAR(32),
                    gender VARCHAR(32),
                    eye_color VARCHAR(32),
                    hair_color VARCHAR(32),
                    height INTEGER,
                    mass REAL,
                    homeworld VARCHAR(64) REFERENCES ex08_planets(name)
                );
            """)
    except psycopg2.Error as error:
        return HttpResponse(str(error), content_type="text/plain; charset=utf-8")
    return HttpResponse("OK", content_type="text/plain; charset=utf-8")


def populate(request):
    sources = [
        ("planets.csv", "ex08_planets", ("name", "climate", "diameter", "orbital_period",
                                        "population", "rotation_period", "surface_water", "terrain")),
        ("people.csv", "ex08_people", ("name", "birth_year", "gender", "eye_color",
                                      "hair_color", "height", "mass", "homeworld")),
    ]
    messages = []
    for filename, table, columns in sources:
        try:
            with connect() as connection, connection.cursor() as cursor:
                with (Path(settings.BASE_DIR) / filename).open(encoding="utf-8") as source:
                    cursor.copy_from(source, table, sep="\t", null="NULL", columns=columns)
            messages.append("OK")
        except (psycopg2.Error, OSError) as error:
            messages.append(f"{filename}: {error}")
    return render(request, "ex08/messages.html", {"messages": messages})


def display(request):
    try:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT people.name, planets.name, planets.climate
                FROM ex08_people AS people
                JOIN ex08_planets AS planets ON people.homeworld = planets.name
                WHERE planets.climate ILIKE %s
                ORDER BY people.name
            """, ["%windy%"])
            rows = cursor.fetchall()
        if rows:
            return render(request, "ex08/table.html", {
                "headers": ["Name", "Homeworld", "Climate"], "rows": rows,
            })
    except psycopg2.Error:
        pass
    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
