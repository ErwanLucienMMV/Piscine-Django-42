# Articles

One cumulative Django 5.2 LTS project for exercises 00-06. The daily instruction to submit a single project takes precedence over the exercise table's usual `ex00/` etc. labels. SQLite is used through Django's ORM. The supplied reference JPEGs are preserved alongside the project.

## Run

Use Python 3.12 or newer, from this directory:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Demo accounts: `alice`, `bob`, `charlie`, each with password `Articles-Demo-42!`. Alice starts with two favourites. Loading the fixture again resets these demo records. The demo users are ordinary accounts; create a separate administrator with `python manage.py createsuperuser` to use the default admin.

The root redirects to the latest articles. Article pages use `/en/articles` and `/fr/articles`; the top-right language link keeps the current page. Account registration, login, personal publications, publishing, favourites and article detail all have named routes. Login is available throughout the menu; logout submits a CSRF-protected POST. Publishing and saving favourites require login, and registration is reserved for anonymous visitors.

## Exercises and checks

- 00: `Article` and `UserFavouriteArticle`, generic article list/home/login, and `articles/fixtures/demo.json` (five articles, three users).
- 01: personal publication and favourite lists, article details, and logout.
- 02: `CreateView` registration, publication and favourite actions; author/user values come from the session.
- 03: shared menu with login errors, newest-first ordering, elapsed times and the `short_synopsis` filter (20 characters including three dots).
- 04: local Bootstrap stylesheet and menu styling based on the supplied reference images; Bootstrap's license is included with the CSS.
- 05: Django locale middleware, language-prefixed named URLs, French gettext catalog, localized dates and menu text. Article data and the site name stay unchanged.
- 06: explicit Django tests in `articles/tests.py` cover required access restrictions and duplicate favourites, as well as publication ownership, forged POST fields, CSRF, authentication, fixtures, translations and view classes.

Run the submitted tests and configuration checks with:

```sh
python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run
```

The compiled French catalog (`django.mo`) is committed, so gettext is not needed to run the site. To edit translations, install GNU gettext, update `locale/fr/LC_MESSAGES/django.po` and run `python manage.py compilemessages` from this directory. Both CSS files are local; pages do not depend on a CDN. Standard Django admin remains available at `/admin/`.

The default configuration is for local coursework. `DJANGO_DB_PATH`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` can override the database path, development secret, debug mode and allowed hosts. Use the required virtual machine and shared host/guest folder during evaluation.
