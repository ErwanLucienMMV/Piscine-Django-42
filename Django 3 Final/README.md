# d09: AJAX accounts and WebSocket chat

The five exercises extend one cumulative Django project, `d09/`, as required by
the day's rules. Use Python 3.12, Django 5.2 LTS, Channels and Daphne. jQuery 3.7.1
is included locally with its MIT license; it is the only frontend JavaScript
library. Chat uses the browser's native WebSocket API.

## Run

From this directory on Linux or macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirement.txt
cd d09
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000 --noreload
```

On Windows PowerShell, create the environment with `py -3.12 -m venv .venv`
and activate it with `.\.venv\Scripts\Activate.ps1`, then run the same `python`
commands. `requirement.txt` was produced by `python -m pip freeze` in the runtime
environment, without browser-testing dependencies.

Visit <http://127.0.0.1:8000/account> to log in, and
<http://127.0.0.1:8000/chat/> to choose a room. The migration creates exactly three
initial rooms: General, Python and Django. Their names are stored in SQLite;
the database is created locally and is not submitted. The unchanged Django admin
at <http://127.0.0.1:8000/admin/> can create further users and manage room names.
For a demonstration, create two accounts, then use separate browser profiles or
private windows to join the same room.

## Behavior

- **00:** `/account` renders the current session state. Login and logout submit
  POST requests through jQuery AJAX with CSRF protection. Errors and the two
  account states update without refreshing the document. A manual refresh
  retains the correct state.
- **01:** Only authenticated users can open the room list, room pages or
  WebSockets. Each message is appended to every participant's conversation,
  including its sender, with the authenticated username. Joining appends
  `<username> has joined the chat`, including for the joining connection.
- **02:** Messages persist in the database. A new connection receives exactly
  the last three posted messages for that room, oldest first, before live events.
  Join and leave notices are not part of this message history.
- **03:** A separate connected-user list includes the current user and updates
  as users enter or leave. Multiple tabs for one account show one username;
  the departure notice appears when that account's last connection leaves.
- **04:** The message container has fixed width and height, scrolls on overflow,
  and moves to the bottom whenever history, a message or a notice is appended.
  Earlier messages stay in the document throughout the connection.

The server derives message authors from Django sessions, checks sessions again
on incoming and outgoing events, rejects foreign WebSocket origins, and closes
the session's chat sockets after AJAX logout. All usernames and message text are
rendered as text. Chat traffic, including history and presence, uses WebSockets;
there is no AJAX polling. A per-room lock serializes publications, joins and
departures so a connection cannot miss or duplicate messages between its initial
history and live stream.

## Runtime and configuration

Run **one ASGI server process**: Daphne's `runserver` command is enabled by the
first installed app. The in-memory channel layer and presence registry are local
to that process. They need no Redis service and clear on restart; posted messages
remain in SQLite. Multiple server processes would require a shared channel layer
and shared presence coordination. The supplied configuration targets the local
exercise, not a multi-process deployment.

`python manage.py check` checks configuration, and
`python manage.py makemigrations --check --dry-run` checks migration consistency.
`python manage.py collectstatic --noinput` collects the vendored assets.

`DJANGO_DB_PATH` selects a different SQLite file. The defaults are for local
development. A deployment must set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`,
`DJANGO_ALLOWED_HOSTS` (comma-separated hosts), configure HTTPS/secure cookies,
and serve collected static files through its web server.

The subject's virtual machine, host/guest shared folder, cluster access and
peer-evaluation setup must be prepared and verified in the evaluation environment.
