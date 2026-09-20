from django.db import migrations


def update_team_bios(apps, schema_editor):
    TeamMember = apps.get_model("core", "TeamMember")

    bios = {
        "Blake Bowman": {
            "bio": (
                "It was in his hometown of Mount Airy that Blake first met his "
                "best friend and future wife, Amber, to whom he has now been "
                "married for 17 years. Along with their two wonderful kids, the "
                "Bowmans have served as missionaries and church planters in Egypt "
                "and Mexico. Blake's time overseas has only deepened his conviction "
                "that God's design for gospel advance is centered on local "
                "churches - churches that faithfully proclaim His Word, make "
                "disciples, and raise up gospel heralds who plant new churches "
                "among every people and in every place. And it is that same "
                "conviction that has led him back home to plant Sojourn Church."
            ),
            "bio_es": (
                "Fue en su ciudad natal de Mount Airy donde Blake conoció por "
                "primera vez a su mejor amiga y futura esposa, Amber, con quien "
                "lleva 17 años casado. Junto con sus dos hijos, los Bowman han "
                "servido como misioneros y plantadores de iglesias en Egipto y "
                "México. El tiempo de Blake en el extranjero solo ha profundizado "
                "su convicción de que el diseño de Dios para el avance del evangelio "
                "se centra en las iglesias locales: iglesias que proclaman fielmente "
                "su Palabra, hacen discípulos y levantan mensajeros del evangelio "
                "que plantan nuevas iglesias entre todos los pueblos y en todo lugar. "
                "Esa misma convicción lo ha llevado de vuelta a casa para plantar la "
                "Iglesia Sojourn."
            ),
        },
        "Ethan Hooker": {
            "bio": (
                "Ethan is passionate about expository preaching, biblical theology, "
                "and discipleship, and has given his life to equipping the local "
                "church to faithfully fulfill the Great Commission. Along the way, "
                "he's worked in emergency medical services and social services "
                "before sensing God's call into pastoral ministry, and has since "
                "earned a B.A. in Biblical Studies and an M.A. in Ministry from "
                "Carolina University, and is currently pursuing a Doctor of Ministry "
                "degree. Along with his wife, Allison, and their two children, Pastor "
                "Ethan longs to see a church centered on Christ, shaped by the Word, "
                "committed to discipleship, and faithfully engaged in the mission of God."
            ),
            "bio_es": (
                "Ethan tiene pasión por la predicación expositiva, la teología bíblica "
                "y el discipulado, y ha dedicado su vida a equipar a la iglesia local "
                "para cumplir fielmente la Gran Comisión. En el camino, trabajó en "
                "servicios médicos de emergencia y servicios sociales antes de sentir "
                "el llamado de Dios al ministerio pastoral. Desde entonces obtuvo una "
                "licenciatura en Estudios Bíblicos y una maestría en Ministerio de "
                "Carolina University, y actualmente cursa un Doctorado en Ministerio. "
                "Junto con su esposa, Allison, y sus dos hijos, el pastor Ethan anhela "
                "ver una iglesia centrada en Cristo, formada por la Palabra, comprometida "
                "con el discipulado y fielmente involucrada en la misión de Dios."
            ),
        },
    }

    for name, values in bios.items():
        TeamMember.objects.filter(name=name).update(**values)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_update_about_beliefs_language"),
    ]

    operations = [
        migrations.RunPython(update_team_bios, migrations.RunPython.noop),
    ]
