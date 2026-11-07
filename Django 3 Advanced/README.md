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

The default configuration is for local coursework. `DJANGO_DB_PATH`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` can override the database path, development secret, debug mode and allowed hosts. Use the required virtual machine and shared host/guest folder during evaluation.
