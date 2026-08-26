from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("communications", "0002_emailrecipient_unsubscribe_emailtemplate")]

    operations = [
        migrations.AddField(
            model_name="emailtemplate",
            name="body_html",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Optional safe HTML for the main message body. Use paragraphs, "
                    "headings, lists, links, strong, and emphasis."
                ),
            ),
        ),
    ]
