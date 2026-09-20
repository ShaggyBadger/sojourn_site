from django.db import migrations


def update_about_mission_vision(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    AboutSection = apps.get_model("core", "AboutSection")

    page = AboutPage.objects.filter(pk=1).first()
    if page is None:
        return

    sections = {
        "intro": {
            "body_en": (
                "At Sojourn, we believe the highest end of the Christian life is "
                "not duty but delight - to know God and enjoy Him forever. "
                "Therefore, we aim to be a church that delights in God in every "
                "area of life."
            ),
            "body_es": (
                "En Sojourn, creemos que el fin supremo de la vida cristiana no es "
                "el deber, sino el deleite: conocer a Dios y disfrutar de Él para "
                "siempre. Por eso, procuramos ser una iglesia que se deleita en "
                "Dios en cada área de la vida."
            ),
        },
        "mission": {
            "body_en": (
                "Sojourn Church exists to delight in God and to help others do the "
                "same."
            ),
            "body_es": (
                "La Iglesia Sojourn existe para deleitarse en Dios y ayudar a otros "
                "a hacer lo mismo."
            ),
        },
    }

    for key, values in sections.items():
        AboutSection.objects.filter(page=page, key=key).update(**values)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_update_team_bios_from_prospectus"),
    ]

    operations = [
        migrations.RunPython(update_about_mission_vision, migrations.RunPython.noop),
    ]
