from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_sitesettings_workshop_theme"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label_en", models.CharField(max_length=100)),
                ("label_es", models.CharField(blank=True, max_length=100)),
                ("url", models.CharField(max_length=500)),
                (
                    "icon",
                    models.CharField(
                        choices=[
                            ("facebook", "Facebook"),
                            ("email", "Email"),
                            ("instagram", "Instagram"),
                            ("youtube", "YouTube"),
                            ("generic", "Generic link"),
                        ],
                        default="generic",
                        max_length=20,
                    ),
                ),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                (
                    "site_settings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_links",
                        to="core.sitesettings",
                    ),
                ),
            ],
            options={
                "verbose_name": "social link",
                "verbose_name_plural": "social links",
                "ordering": ("display_order", "pk"),
            },
        ),
    ]
