from django.db import migrations


def clear_duplicate_seventh_icon(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    site_settings = SiteSettings.objects.filter(pk=1).first()
    if site_settings and site_settings.homepage_icon_7_asset_id == site_settings.homepage_icon_8_asset_id:
        site_settings.homepage_icon_7_asset_id = None
        site_settings.save(update_fields=("homepage_icon_7_asset",))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_expand_homepage_distinctives"),
    ]

    operations = [
        migrations.RunPython(clear_duplicate_seventh_icon, migrations.RunPython.noop),
    ]
