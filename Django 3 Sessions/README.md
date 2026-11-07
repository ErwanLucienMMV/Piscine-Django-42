# Life Pro Tips

The seven exercises share the cumulative project in `ex/`. It uses Python 3.11+
(Python 3.12 recommended), Django 5.2 LTS and django-bootstrap5. Bootstrap 5.3.8
CSS is included locally, so the interface does not require a CDN connection.

## Run

From this directory, on Linux or macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r ex/requirements.txt
cd ex
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, create the environment with `py -3 -m venv .venv` and
activate it with `.\.venv\Scripts\Activate.ps1`, then use the same `python`
commands. Visit <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/admin/>.
SQLite creates its database locally on the first migration; no database is
submitted. `python manage.py check` checks the project configuration.

## Exercises

- **00:** Each anonymous session receives one of the ten names in `settings.py`.
  Its fixed 42-second deadline is independent of page refreshes and login
  sessions. The next visited page immediately displays a fresh name after expiry.
- **01:** Register, log in and log out through the navigation bar. Registration
  immediately activates and signs in the user. Authenticated visitors are
  redirected away from registration and login. Password fields remain masked
  and are cleared after validation errors.
- **02:** Logged-in users post tips through a ModelForm on the home page. Every
  visitor sees the content, author and creation date of every tip.
- **03:** Voting uses one database row per user and tip, with unique and value
  constraints. Repeating a vote removes it; choosing the opposite vote replaces
  it. Counts are calculated from existing votes. Every action redirects home.
- **04:** `tips.delete_tip` permits deleting other users' tips. Authors may always
  delete their own tips. Manage individual or group grants in the admin.
- **05:** The custom `tips.downvote_tip` permission controls downvotes on other
  users' tips. Authors may downvote their own tips. Both permissions are checked
  by the server as well as reflected in the available buttons.
- **06:** The custom user model calculates reputation from votes on authored
  tips: +5 per upvote and -2 per downvote, starting at zero. At 15 points the
  user gains downvoting, and at 30 points deletion of other users' tips. Earned
  permissions disappear immediately when reputation falls below their threshold.
  Explicit admin/group grants remain independent of earned permissions. Deleting
  a tip removes its votes and their reputation contribution. Reputation appears
  beside usernames, including in the navigation bar and admin.

Mutation routes accept POST with CSRF protection. The routes are `/`,
`/register/`, `/login/`, `/logout/`, `/tips/<id>/vote/up/`,
`/tips/<id>/vote/down/` and `/tips/<id>/delete/`.

The custom user is configured from the initial migration to avoid changing the
user table halfway through an existing database. The Git history records the
successive exercise checkpoints.

## Configuration

The defaults are for local development. `DJANGO_DB_PATH` selects a different
SQLite database. For deployment, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` and
`DJANGO_ALLOWED_HOSTS` (comma-separated hosts), configure HTTPS and secure cookies,
and serve files from `python manage.py collectstatic` through the web server.
The subject's virtual-machine/shared-folder and peer-evaluation requirements
must be prepared in the evaluation environment.

Bootstrap is distributed under its MIT license; see
`ex/tips/static/tips/bootstrap.LICENSE`.
