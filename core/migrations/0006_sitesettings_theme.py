from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_update_about_beliefs"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="theme",
            field=models.CharField(
                choices=[
                    ("dark", "Dark"),
                    ("light", "Light"),
                    ("medium", "Medium"),
                ],
                default="dark",
                help_text="Choose the visual theme for the entire public website.",
                max_length=10,
            ),
        ),
    ]
