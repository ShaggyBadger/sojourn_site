from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("sermons", "0002_normalize_transcripts")]

    operations = [
        migrations.CreateModel(
            name="SermonTranslation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("es", "Spanish")], max_length=10)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("summary", models.TextField(blank=True)),
                ("thesis", models.TextField(blank=True)),
                ("transcript", models.TextField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sermon", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="translations", to="sermons.sermon")),
            ],
        ),
        migrations.CreateModel(
            name="TranslationJob",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("es", "Spanish")], max_length=10)),
                ("field", models.CharField(max_length=20)),
                ("source_text", models.TextField()),
                ("source_hash", models.CharField(max_length=64)),
                ("token_hash", models.CharField(max_length=128)),
                ("status", models.CharField(choices=[("claimed", "Claimed"), ("completed", "Completed"), ("expired", "Expired")], default="claimed", max_length=12)),
                ("claimed_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("sermon", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="translation_jobs", to="sermons.sermon")),
            ],
        ),
        migrations.AddConstraint(
            model_name="sermontranslation",
            constraint=models.UniqueConstraint(fields=("sermon", "language"), name="unique_sermon_translation_language"),
        ),
        migrations.AddConstraint(
            model_name="translationjob",
            constraint=models.UniqueConstraint(condition=models.Q(status="claimed"), fields=("sermon", "language", "field", "status"), name="one_active_translation_job"),
        ),
    ]
