from django.db import migrations


def update_about_beliefs(apps, schema_editor):
    AboutSection = apps.get_model("core", "AboutSection")

    AboutSection.objects.filter(page_id=1, key="beliefs").update(
        body_en=(
            "We affirm the historic Christian faith expressed in the "
            "Apostles' Creed. Our teaching is also shaped by the New Hampshire "
            "Confession of Faith and the Heidelberg Catechism. Together, these "
            "documents help us understand and faithfully communicate what we "
            "believe about God, Scripture, salvation, the church, and Christian "
            "living."
        ),
        body_es=(
            "Afirmamos la fe cristiana histórica expresada en el Credo de los "
            "Apóstoles. Nuestra enseñanza también se forma por la Confesión de "
            "Fe de New Hampshire y el Catecismo de Heidelberg. Juntos, estos "
            "documentos nos ayudan a entender y comunicar fielmente lo que "
            "creemos acerca de Dios, las Escrituras, la salvación, la iglesia y "
            "la vida cristiana."
        ),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_update_about_branding"),
    ]

    operations = [
        migrations.RunPython(update_about_beliefs, migrations.RunPython.noop),
    ]
