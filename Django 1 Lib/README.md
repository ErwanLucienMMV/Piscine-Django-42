# Django 1 - Librairies

Use Python 3.12 or newer and Bash in the evaluation virtual machine. Keep the
repository in the shared host/VM directory. Run each command from the indicated
exercise directory. Dependencies, generated articles, logs and environments are
ignored by Git.

## ex00 - Antigravity

```bash
python3 geohashing.py 37 -122 2005-05-26-10458.68
```

The third argument combines a calendar date and the Dow Jones opening value.
Python's standard `antigravity` module prints the coordinates; importing this
module also opens the original xkcd comic in the default browser.

## ex01 - Pip

```bash
bash my_script.sh
```

Requires Git and pip. The script prints the pip version, installs the development
branch of [path (formerly path.py)](https://github.com/jaraco/path) in `local_lib`,
records installation details in `install.log`, and runs `my_program.py` with that
directory first on `PYTHONPATH`. Repeated runs upgrade the local installation.
The program creates `example/hello.txt`, writes text and prints the file contents.
Set `PYTHON` to select another Python 3 interpreter if needed.

## ex02 - Wikipedia API

```bash
python3 -m pip install -r requirement.txt
python3 request_wikipedia.py "chocolatine"
```

Uses the English Wikipedia API search, including suggested spelling corrections,
retrieves the article's wiki source, and converts it to plain text with `dewiki`.
The result is written as `chocolatine.wiki` in the working directory. Spaces and
characters unsuitable for filenames become underscores. Invalid searches and
network/API errors print an error before opening an output file.

## ex03 - Roads to philosophy

```bash
python3 -m pip install -r requirement.txt
python3 roads_to_philosophy.py "42 (number)"
```

Retrieves ordinary English Wikipedia HTML pages through browser search URLs,
parses article titles and HTML redirects, and follows the first article link in
the introduction. In accordance with the exercise's explicit rules, links in
italics or parentheses can be followed; links to help, categories, external sites,
page fragments and references are ignored. Each visited title is printed. The
successful count includes the starting article, redirects and Philosophy.
Loops, dead ends and network errors terminate the program. Wikipedia content
changes, so the example's historical 17-article route is not guaranteed.

## ex04 - Virtualenv

Install the platform's Python development headers, C compiler and PostgreSQL
development libraries first (for example `python3-dev`, `build-essential` and
`libpq-dev` on Debian/Ubuntu). `pg_config` must be available on `PATH` to build
`psycopg2` from source.

```bash
source my_script.sh
python -m django --version
```

Source the script in Bash so `django_venv` stays active in that shell. Executing
it as a child process cannot activate its parent shell and prints usage instead.
The environment lives beside the script even when sourced from another directory.

The requirement file pins the latest stable versions checked on 2026-11-07:
[Django 6.1.3](https://www.djangoproject.com/download/) and
[psycopg2 2.9.13](https://pypi.org/project/psycopg2/).

## ex05 - Hello World

With the environment from ex04 active:

```bash
cd ../ex05
python manage.py check
python manage.py runserver 127.0.0.1:8000
```

Open <http://localhost:8000/helloworld> to see `Hello World !`. Alternatively,
install this exercise's `requirement.txt` in your own environment. This minimal
project needs no database or migrations. The development settings allow localhost
and loopback addresses.
