"""Load the supplied fixture, adapting its numeric planet references to names."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Load ex10_initial_data.json with homeworld references to Planets.name."

    def add_arguments(self, parser):
        parser.add_argument("fixture", nargs="?", type=Path,
                            default=settings.BASE_DIR / "ex10_initial_data.json")

    def handle(self, *args, **options):
        try:
            records = json.loads(options["fixture"].read_text(encoding="utf-8"))
            planets = {
                record["pk"]: record["fields"]["name"]
                for record in records if record["model"] == "ex10.planets"
            }
            now = timezone.now().isoformat()
            for record in records:
                if record["model"] not in {'ex10.people', 'ex10.planets', 'ex10.movies'}:
                    raise ValueError(f"Unexpected model: {record['model']}")
                fields = record["fields"]
                if record["model"] == "ex10.people" and fields.get("homeworld") is not None:
                    fields["homeworld"] = planets[fields["homeworld"]]
                if record["model"] in {"ex10.planets", "ex10.people"}:
                    for field in ["created", "updated"]:
                        value = parse_datetime(fields.get(field, now))
                        if value is None:
                            raise ValueError(f"Invalid {field} timestamp")
                        if timezone.is_naive(value):
                            value = timezone.make_aware(value)
                        fields[field] = value.isoformat()
            # Django's fixture loader validates relations and resets generated-key sequences.
            with TemporaryDirectory(prefix="ex10-fixture-") as directory:
                adapted = Path(directory) / "adapted.json"
                adapted.write_text(json.dumps(records), encoding="utf-8")
                with transaction.atomic():
                    call_command("loaddata", str(adapted), verbosity=0)
        except (OSError, ValueError, KeyError, TypeError, DatabaseError,
                CommandError) as error:
            raise CommandError(f"Could not load fixture: {error}") from error
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(records)} objects."))
