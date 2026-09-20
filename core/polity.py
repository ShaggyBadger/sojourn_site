"""Bilingual content for the public How We Are Led page."""


POLITY_CONTENT = {
    "title": "How We Are Led",
    "title_es": "Cómo somos guiados",
    "description": (
        "Learn how Sojourn Church understands biblical leadership: elder-led, "
        "deacon-served, and congregationally ruled."
    ),
    "description_es": (
        "Conoce cómo Iglesia Sojourn entiende el liderazgo bíblico: guiada por "
        "ancianos, servida por diáconos y gobernada por la congregación."
    ),
    "intro": (
        "Christ is the head of his church, so we want our leadership structure to "
        "reflect what he has prescribed in his Word."
    ),
    "intro_es": (
        "Cristo es la cabeza de su iglesia, por eso queremos que nuestra estructura "
        "de liderazgo refleje lo que él ha establecido en su Palabra."
    ),
    "sections": (
        {
            "title": "Elder-Led",
            "title_es": "Guiada por ancianos",
            "body": (
                "Scripture calls churches to be shepherded by a plurality of qualified "
                "elders, also called pastors or overseers. They teach the Word, guard "
                "sound doctrine, and shepherd the souls entrusted to them."
            ),
            "body_es": (
                "Las Escrituras llaman a las iglesias a ser pastoreadas por una pluralidad "
                "de ancianos calificados, también llamados pastores u obispos. Ellos enseñan "
                "la Palabra, guardan la sana doctrina y pastorean las almas que les han sido confiadas."
            ),
            "references": "1 Timothy 3:1-7; Titus 1:5-9; Acts 20:28; Hebrews 13:17; 1 Peter 5:1-4",
            "references_es": "1 Timoteo 3:1-7; Tito 1:5-9; Hechos 20:28; Hebreos 13:17; 1 Pedro 5:1-4",
        },
        {
            "title": "Deacon-Served",
            "title_es": "Servida por diáconos",
            "body": (
                "Alongside elders, Scripture establishes the office of deacon: qualified "
                "servants who care for practical needs so that the ministry of the Word "
                "and prayer is not neglected. Deacons serve the church; they are not a separate governing body."
            ),
            "body_es": (
                "Junto con los ancianos, las Escrituras establecen el oficio de diácono: "
                "siervos calificados que atienden las necesidades prácticas para que no se descuiden "
                "el ministerio de la Palabra y la oración. Los diáconos sirven a la iglesia; no son un cuerpo gobernante separado."
            ),
            "references": "Acts 6:1-6; 1 Timothy 3:8-13",
            "references_es": "Hechos 6:1-6; 1 Timoteo 3:8-13",
        },
        {
            "title": "Congregationally-Ruled",
            "title_es": "Gobernada por la congregación",
            "body": (
                "While elders lead and deacons serve, final authority under Christ rests "
                "with the gathered congregation, especially in matters such as membership, "
                "discipline, doctrine, and the appointment of church leaders."
            ),
            "body_es": (
                "Mientras los ancianos guían y los diáconos sirven, la autoridad final bajo "
                "Cristo reside en la congregación reunida, especialmente en asuntos como la membresía, "
                "la disciplina, la doctrina y el nombramiento de los líderes de la iglesia."
            ),
            "references": "Matthew 18:15-17; 1 Corinthians 5:1-5, 12-13; Acts 15:22; Acts 6:3-5",
            "references_es": "Mateo 18:15-17; 1 Corintios 5:1-5, 12-13; Hechos 15:22; Hechos 6:3-5",
        },
    ),
}


def get_polity_page(language="en"):
    """Return the How We Are Led page localized to the active language."""
    is_spanish = (language or "en").split("-")[0] == "es"
    suffix = "_es" if is_spanish else ""
    return {
        "title": POLITY_CONTENT[f"title{suffix}"],
        "description": POLITY_CONTENT[f"description{suffix}"],
        "intro": POLITY_CONTENT[f"intro{suffix}"],
        "sections": tuple(
            {
                "title": section[f"title{suffix}"],
                "body": section[f"body{suffix}"],
                "references": section[f"references{suffix}"],
            }
            for section in POLITY_CONTENT["sections"]
        ),
    }
