from django.db import migrations


def update_about_beliefs_language(apps, schema_editor):
    AboutSection = apps.get_model("core", "AboutSection")

    AboutSection.objects.filter(page_id=1, key="beliefs").update(
        body_en=(
            "We officially affirm the Apostles' Creed and the New Hampshire "
            "Confession of Faith. We also learn from historic Christian "
            "documents, including catechisms and confessions such as the "
            "Heidelberg Catechism, as helpful resources for understanding and "
            "communicating the faith."
        ),
        body_es=(
            "Afirmamos oficialmente el Credo de los Apóstoles y la Confesión de "
            "Fe de New Hampshire. También aprendemos de documentos cristianos "
            "históricos, incluidos catecismos y confesiones como el Catecismo de "
            "Heidelberg, como recursos útiles para entender y comunicar la fe."
        ),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_sitesettings_workshop_theme"),
    ]

    operations = [
        migrations.RunPython(update_about_beliefs_language, migrations.RunPython.noop),
    ]
