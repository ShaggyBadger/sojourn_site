import re

from django.db import migrations


def normalize_transcripts(apps, schema_editor):
    sermon_model = apps.get_model("sermons", "Sermon")

    for sermon in sermon_model.objects.exclude(transcript="").iterator():
        normalized = sermon.transcript.replace("\r\n", "\n").replace("\r", "\n")
        normalized = re.sub(r"[ \t]*\n[ \t]*", "\n\n", normalized)
        normalized = re.sub(r"\n{2,}", "\n\n", normalized).strip()
        if normalized != sermon.transcript:
            sermon.transcript = normalized
            sermon.save(update_fields=("transcript",))


class Migration(migrations.Migration):
    dependencies = [("sermons", "0001_initial")]

    operations = [migrations.RunPython(normalize_transcripts, migrations.RunPython.noop)]
