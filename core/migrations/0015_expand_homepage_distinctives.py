from django.db import migrations, models


STATEMENTS_EN = (
    "God-Centered",
    "Word-Driven",
    "On Mission",
    "Supernatural Community",
    "Desperately Dependent",
    "Made Holy by Grace",
    "Conspicuously Joyful",
    "Journeying Homeward",
)

STATEMENTS_ES = (
    "Centrados en Dios",
    "Guiados por la Palabra",
    "En misión",
    "Comunidad sobrenatural",
    "Desesperadamente dependientes",
    "Santificados por la gracia",
    "Visiblemente gozosos",
    "Caminando hacia el hogar",
)

DETAILS_EN = (
    "We do everything for the glory of God. His pleasure and glory shape our decisions, our worship, and our life together as a church.",
    "We take our direction from the Bible rather than convenience or cultural pressure. Scripture should shape our worship, outreach, structure, and programs.",
    "We take Jesus' command to make disciples seriously. We want overlooked and underreached neighbors to know and enjoy Christ, near and far.",
    "We want to display the reconciling power of the gospel through a diverse people united by a common love for Christ.",
    "Apart from Christ we can do nothing. We depend on God in prayer because he alone saves sinners and builds his church.",
    "Grace does not leave us unchanged. We want to walk in holiness, pursue accountability, and live as people who have been transformed by Christ.",
    "We have every reason to rejoice in Christ. We want that joy to be visible in our singing, preaching, prayer, fellowship, and daily lives.",
    "This world is not our final home. We want to live with a pilgrim's hope, storing up treasure in heaven and looking forward to dwelling with God forever.",
)

DETAILS_ES = (
    "Hacemos todo para la gloria de Dios. Su placer y su gloria dan forma a nuestras decisiones, nuestra adoración y nuestra vida juntos como iglesia.",
    "Recibimos nuestra dirección de la Biblia y no de la conveniencia ni de la presión cultural. Las Escrituras deben formar nuestra adoración, nuestro alcance, nuestra estructura y nuestros programas.",
    "Tomamos en serio el mandato de Jesús de hacer discípulos. Queremos que nuestros vecinos olvidados y poco alcanzados conozcan y disfruten a Cristo, cerca y lejos.",
    "Queremos mostrar el poder reconciliador del evangelio mediante un pueblo diverso unido por un amor común por Cristo.",
    "Separados de Cristo no podemos hacer nada. Dependemos de Dios en oración porque solo él salva a los pecadores y edifica su iglesia.",
    "La gracia no nos deja sin cambio. Queremos caminar en santidad, buscar la responsabilidad mutua y vivir como personas transformadas por Cristo.",
    "Tenemos toda razón para gozarnos en Cristo. Queremos que ese gozo sea visible en nuestros cantos, predicación, oración, compañerismo y vida diaria.",
    "Este mundo no es nuestro hogar final. Queremos vivir con la esperanza de peregrinos, acumulando tesoros en el cielo y esperando morar con Dios para siempre.",
)


def seed_homepage_distinctives(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    site_settings = SiteSettings.objects.filter(pk=1).first()
    if not site_settings:
        return

    updates = {}
    for number, values in enumerate(zip(STATEMENTS_EN, STATEMENTS_ES, DETAILS_EN, DETAILS_ES), start=1):
        statement_en, statement_es, detail_en, detail_es = values
        updates.update(
            {
                f"homepage_statement_{number}_en": statement_en,
                f"homepage_statement_{number}_es": statement_es,
                f"homepage_detail_{number}_en": detail_en,
                f"homepage_detail_{number}_es": detail_es,
            }
        )

    # The former seventh slot was the final existing distinctive; preserve its
    # assigned media asset while making room for the new seventh item.
    updates["homepage_icon_8_asset_id"] = site_settings.homepage_icon_7_asset_id
    SiteSettings.objects.filter(pk=site_settings.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_update_about_beliefs_documents"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="homepage_icon_8_asset",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.PROTECT,
                related_name="homepage_icon_8_site_settings",
                to="media.mediaasset",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="homepage_statement_8_en",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="homepage_statement_8_es",
            field=models.CharField(blank=True, max_length=255),
        ),
    ] + [
        migrations.AddField(
            model_name="sitesettings",
            name=f"homepage_detail_{number}_{language}",
            field=models.TextField(blank=True),
        )
        for number in range(1, 9)
        for language in ("en", "es")
    ] + [
        migrations.RunPython(seed_homepage_distinctives, migrations.RunPython.noop),
    ]
