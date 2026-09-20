from django.db import migrations


def update_about_beliefs_documents(apps, schema_editor):
    AboutSection = apps.get_model("core", "AboutSection")

    AboutSection.objects.filter(page_id=1, key="beliefs").update(
        body_en=(
            "We affirm the historic Christian faith expressed in the Apostles' "
            "Creed and the Nicene Creed. As a Baptist church, our teaching is "
            "also shaped by the Baptist Faith and Message 2000 and the New "
            "Hampshire Confession of Faith. Together, these documents help us "
            "understand and faithfully communicate what we believe about God, "
            "Scripture, salvation, the church, and Christian living."
        ),
        body_es=(
            "Afirmamos la fe cristiana histórica expresada en el Credo de los "
            "Apóstoles y el Credo Niceno. Como iglesia bautista, nuestra enseñanza "
            "también se forma por Fe y Mensaje Bautistas 2000 y la Confesión de Fe "
            "de New Hampshire. Juntos, estos documentos nos ayudan a entender y "
            "comunicar fielmente lo que creemos acerca de Dios, las Escrituras, "
            "la salvación, la iglesia y la vida cristiana."
        ),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_update_about_mission_vision"),
    ]

    operations = [
        migrations.RunPython(update_about_beliefs_documents, migrations.RunPython.noop),
    ]
