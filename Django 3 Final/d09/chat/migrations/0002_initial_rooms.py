from django.db import migrations


def create_rooms(apps, schema_editor):
    Room = apps.get_model("chat", "Room")
    for name in ("General", "Python", "Django"):
        Room.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [("chat", "0001_initial")]
    operations = [migrations.RunPython(create_rooms, migrations.RunPython.noop)]
