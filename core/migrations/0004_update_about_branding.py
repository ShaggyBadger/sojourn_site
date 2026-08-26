from django.db import migrations


def update_about_content(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    AboutSection = apps.get_model("core", "AboutSection")

    page = AboutPage.objects.filter(pk=1).first()
    if page is None:
        return

    page.title_en = "About Sojourn Church"
    page.title_es = "Acerca de Iglesia Sojourn"
    page.meta_description_en = (
        "Learn about Sojourn Church, our beliefs, bilingual ministry, "
        "and pastoral leadership."
    )
    page.meta_description_es = (
        "Conoce Iglesia Sojourn, nuestras creencias, nuestro ministerio "
        "bilingüe y nuestro liderazgo pastoral."
    )
    page.save(
        update_fields=(
            "title_en",
            "title_es",
            "meta_description_en",
            "meta_description_es",
        )
    )

    sections = {
        "intro": {
            "body_en": (
                "Sojourn Church is a Christian church learning to walk "
                "faithfully together as a fully bilingual church in our local "
                "community."
            ),
            "body_es": (
                "Iglesia Sojourn es una iglesia cristiana que aprende a caminar "
                "fielmente como una iglesia plenamente bilingüe en nuestra "
                "comunidad local."
            ),
        },
        "mission": {
            "body_en": (
                "Sojourn Church exists to worship Jesus Christ, grow together "
                "in faith, and serve our local community as a fully bilingual "
                "church, with a particular desire to welcome and reach our "
                "Latino neighbors."
            ),
            "body_es": (
                "Iglesia Sojourn existe para adorar a Jesucristo, crecer juntos "
                "en la fe y servir a nuestra comunidad local como una iglesia "
                "plenamente bilingüe, con un deseo especial de dar la bienvenida "
                "y alcanzar a nuestros vecinos latinos."
            ),
        },
        "beliefs": {
            "body_en": (
                "We affirm the historic Christian faith expressed in the "
                "Apostles' Creed and the Nicene Creed. Our teaching is also "
                "shaped by the New Hampshire Confession of Faith and the "
                "Heidelberg Catechism. Together, these documents help us "
                "understand and faithfully communicate what we believe about "
                "God, Scripture, salvation, the church, and Christian living."
            ),
            "body_es": (
                "Afirmamos la fe cristiana histórica expresada en el Credo de "
                "los Apóstoles y el Credo Niceno. Nuestra enseñanza también se "
                "forma por la Confesión de Fe de New Hampshire y el Catecismo "
                "de Heidelberg. Juntos, estos documentos nos ayudan a entender "
                "y comunicar fielmente lo que creemos acerca de Dios, las "
                "Escrituras, la salvación, la iglesia y la vida cristiana."
            ),
        },
    }

    for key, values in sections.items():
        AboutSection.objects.filter(page_id=page.pk, key=key).update(**values)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_aboutpage_aboutsection"),
    ]

    operations = [
        migrations.RunPython(update_about_content, migrations.RunPython.noop),
    ]
