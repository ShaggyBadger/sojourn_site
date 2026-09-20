"""Bilingual content for the Partner With Us page."""


PARTNER_CONTENT = {
    "title": "Partner With Us",
    "title_es": "Colabora con nosotros",
    "description": (
        "Discover four ways to partner with Sojourn Church in planting a bilingual "
        "church in Mount Airy: connect, pray, give, and go."
    ),
    "description_es": (
        "Descubre cuatro maneras de colaborar con Iglesia Sojourn para plantar una "
        "iglesia bilingüe en Mount Airy: conectar, orar, dar e ir."
    ),
    "intro": (
        "Sojourn Church is being planted through the prayers, generosity, presence, "
        "and service of God's people. There is a place for you to join us."
    ),
    "intro_es": (
        "Iglesia Sojourn está siendo plantada mediante las oraciones, la generosidad, "
        "la presencia y el servicio del pueblo de Dios. Hay un lugar para que te unas a nosotros."
    ),
    "ways": (
        {
            "title": "Connect",
            "title_es": "Conecta",
            "body": (
                "Do you know someone in or near Mount Airy who would benefit from being "
                "part of Sojourn Church? We would love to connect with them and share more "
                "about who we are."
            ),
            "body_es": (
                "¿Conoces a alguien que vive en Mount Airy o cerca de allí y que podría "
                "beneficiarse de ser parte de Iglesia Sojourn? Nos encantaría conectar con esa "
                "persona y compartir más sobre quiénes somos."
            ),
            "action": "Email us",
            "action_es": "Escríbenos",
            "url": "mailto:contact@sojourn-church.com",
        },
        {
            "title": "Pray",
            "title_es": "Ora",
            "body": (
                "We need God's presence and power to establish his church in Mount Airy. "
                "Pray that God would draw people to himself, establish this church, and bless "
                "the work of Sojourn Church."
            ),
            "body_es": (
                "Necesitamos la presencia y el poder de Dios para establecer su iglesia en "
                "Mount Airy. Ora para que Dios atraiga a las personas hacia él, establezca esta "
                "iglesia y bendiga la obra de Iglesia Sojourn."
            ),
            "action": "Stay connected for prayer updates",
            "action_es": "Mantente conectado para recibir actualizaciones de oración",
            "url_name": "communications:subscribe",
        },
        {
            "title": "Give",
            "title_es": "Da",
            "body": (
                "We trust God to supply what Sojourn Church needs through the generosity of "
                "his people. Whether through a one-time gift or a recurring commitment, your "
                "giving helps establish and strengthen this church."
            ),
            "body_es": (
                "Confiamos en que Dios suplirá lo que Iglesia Sojourn necesita mediante la "
                "generosidad de su pueblo. Ya sea por medio de una ofrenda única o un compromiso "
                "recurrente, tu donación ayuda a establecer y fortalecer esta iglesia."
            ),
            "action": "Learn about giving",
            "action_es": "Conoce más sobre cómo dar",
            "url_name": "giving",
        },
        {
            "title": "Go",
            "title_es": "Ve",
            "body": (
                "Perhaps God is calling you to join what he is doing in Mount Airy. Reach out "
                "to take your first steps, attend a gathering, meet the team, and see what God "
                "is doing through Sojourn Church."
            ),
            "body_es": (
                "Quizás Dios te está llamando a unirte a lo que está haciendo en Mount Airy. "
                "Escríbenos para dar tus primeros pasos, asistir a una reunión, conocer al equipo "
                "y ver lo que Dios está haciendo por medio de Iglesia Sojourn."
            ),
            "action": "Take your first step",
            "action_es": "Da tu primer paso",
            "url_name": "communications:planting-interest",
        },
    ),
}


def get_partner_page(language="en"):
    """Return the Partner With Us page localized to the active language."""
    is_spanish = (language or "en").split("-")[0] == "es"
    suffix = "_es" if is_spanish else ""
    return {
        "title": PARTNER_CONTENT[f"title{suffix}"],
        "description": PARTNER_CONTENT[f"description{suffix}"],
        "intro": PARTNER_CONTENT[f"intro{suffix}"],
        "ways": tuple(
            {
                "title": way[f"title{suffix}"],
                "body": way[f"body{suffix}"],
                "action": way[f"action{suffix}"],
                "url": way.get("url"),
                "url_name": way.get("url_name"),
            }
            for way in PARTNER_CONTENT["ways"]
        ),
    }
