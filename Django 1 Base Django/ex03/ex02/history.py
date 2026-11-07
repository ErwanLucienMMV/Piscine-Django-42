"""Append-only UTF-8 history, stored in the application's configured log file."""
from datetime import datetime
import json
from pathlib import Path
from threading import Lock

from django.conf import settings
from django.utils import timezone

_write_lock = Lock()


def read_entries():
    path = Path(settings.EX02_LOG_FILE)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    entries = []
    for line in lines:
        try:
            record = json.loads(line)
            timestamp = datetime.fromisoformat(record["timestamp"])
            text = record["text"]
            if not isinstance(text, str) or timezone.is_naive(timestamp):
                continue
        except (ValueError, KeyError, TypeError):
            continue
        entries.append({"timestamp": timestamp, "text": text})
    return entries


def append_entry(text):
    record = {
        "timestamp": timezone.localtime().isoformat(timespec="seconds"),
        "text": text,
    }
    # JSON keeps each submission on a single log line, even if text contains newlines.
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with _write_lock:
        with Path(settings.EX02_LOG_FILE).open("a", encoding="utf-8") as logfile:
            logfile.write(line)
