# Django 2 SQL

Python 3, Django 5.2 LTS and PostgreSQL. The `d05` project contains the independent
`ex00` through `ex10` applications. SQL exercises use psycopg2; ORM exercises use
Django models and querysets.

## Setup

From this directory, create a virtual environment and install `requirements.txt`:

```sh
python3 -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
```

Create the PostgreSQL role and database as a PostgreSQL administrator:

```sh
createuser --pwprompt djangouser
# Enter secret as the password.
createdb --owner=djangouser formationdjango
```

Defaults are `127.0.0.1:5432`, database `formationdjango`, user `djangouser`, password
`secret`. Standard `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD`
environment variables override these values. The database owner must have schema
creation rights. Development hosts are `localhost` and `127.0.0.1`.

The subject excludes submitted migrations. Generate and apply them locally:

```sh
python3 manage.py makemigrations ex01 ex03 ex05 ex07 ex09 ex10
python3 manage.py migrate
python3 manage.py check
python3 manage.py runserver
```

Alternatively, `python3 manage.py migrate --run-syncdb` creates the model tables
directly when no migrations have been generated. Generated migrations are ignored.
SQL tables are created by their own `init` views.

## Exercise routes

URLs match the subject and have **no trailing slash**.

| App | Routes | Storage |
| --- | --- | --- |
| ex00 | `/ex00/init` | SQL movie schema |
| ex01 | Model only | ORM movie schema |
| ex02 | `/ex02/init`, `/ex02/populate`, `/ex02/display` | SQL |
| ex03 | `/ex03/populate`, `/ex03/display` | ORM |
| ex04 | `/ex04/init`, `/ex04/populate`, `/ex04/display`, `/ex04/remove` | SQL |
| ex05 | `/ex05/populate`, `/ex05/display`, `/ex05/remove` | ORM |
| ex06 | `/ex06/init`, `/ex06/populate`, `/ex06/display`, `/ex06/update` | SQL with timestamps and trigger |
| ex07 | `/ex07/populate`, `/ex07/display`, `/ex07/update` | ORM with automatic timestamps |
| ex08 | `/ex08/init`, `/ex08/populate`, `/ex08/display` | SQL COPY and foreign key |
| ex09 | `/ex09/display` | ORM and foreign key |
| ex10 | `/ex10` | ORM search with many-to-many movie characters |

For SQL apps, visit `init` before `populate`. The movie population views insert the
seven specified films and report a result for each insertion. Repeating population
reports duplicate errors for existing rows; removed films are inserted again.
The nullable `opening_crawl` starts as NULL; the supplied `opening_crawl.json`
contains text that can be pasted into the update forms.

Exercise 08 imports `planets.csv` before `people.csv`. These supplied files are
tab-separated, use `NULL` for missing values, and omit generated IDs. Each file
is imported in a transaction; a failed import is rolled back and reported.

Load the original ORM fixtures with:

```sh
python3 manage.py load_ex09
python3 manage.py load_ex10
```

The supplied fixtures encode `homeworld` as a numeric planet ID, while the subject
requires a foreign key to `Planets.name`. These commands translate IDs to names
in a temporary fixture, then use Django's fixture loader to validate relationships
and reset ID sequences. Original resource files stay unchanged. Existing fixture
timestamps are preserved and missing timestamps are initialized. Repeating a load
updates the fixture objects and their associations. Each command also accepts an
optional path to a fixture for that exercise.

For the exercise 10 example, search from `1900-01-01` to `2000-01-01`, with diameter
`11000` and gender `female`. Results show each matching character/movie association;
date bounds and the minimum diameter are inclusive. All four inputs are required.
