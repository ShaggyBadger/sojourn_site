"""Bilingual content for the public beliefs hub and creed pages."""

from .confession import CONFESSION_SOURCE_URL, get_confession_articles


BFM_SOURCE_URL = "https://bfm.sbc.net/"
BFM_SOURCE_ES_URL = "https://bfandm.wpengine.com/es/fe-y-mensaje-bautistas/"


BFM_ARTICLES = (
    ("I. The Scriptures", "The Bible is God's trustworthy revelation and the supreme standard for faith, Christian unity, and human conduct. It points us to Christ and teaches us how God judges and saves."),
    ("II. God", "There is one true, holy, personal, and sovereign God who created and sustains all things. He has revealed himself as Father, Son, and Holy Spirit, distinct in person and united in divine nature."),
    ("III. Man", "Human beings are created in God's image as male and female, possessing dignity and responsibility. Sin has affected every person, and only God's grace can restore us to fellowship with him."),
    ("IV. Salvation", "Salvation is offered freely through Jesus Christ and involves the whole person. God's saving work includes new birth, justification, sanctification, and final glorification, and it is received through personal faith in Christ."),
    ("V. God's Purpose of Grace", "God graciously saves and keeps his people, accomplishing his purposes without denying human responsibility. His grace excludes boasting, produces humility, and enables believers to persevere in faith."),
    ("VI. The Church", "A local church is a covenant community of baptized believers under Christ's lordship, gathered for worship, discipleship, mission, and mutual accountability. Its biblical offices are pastor or elder and deacon."),
    ("VII. Baptism and the Lord's Supper", "Baptism and the Lord's Supper are the church's ordinances. Baptism portrays a believer's union with Christ in his death and resurrection, while the Supper remembers Christ's death and anticipates his return."),
    ("VIII. The Lord's Day", "The first day of the week is set apart for Christian worship and spiritual devotion in remembrance of Jesus' resurrection. Its observance should be shaped by conscience under Christ's lordship."),
    ("IX. The Kingdom", "God rules over all creation, and his saving reign is entered through humble trust in Jesus Christ. Christians pray and work for God's will to be done while awaiting the kingdom's final consummation."),
    ("X. Last Things", "God will bring history to its appointed end. Christ will return visibly, raise the dead, and judge all people; the redeemed will live with him, while the unrighteous face everlasting punishment."),
    ("XI. Evangelism and Missions", "Every Christian and every church shares the privilege and duty of making disciples among all peoples. Gospel proclamation should be supported by a life that reflects the message of Christ."),
    ("XII. Education", "Christian learning seeks wisdom under the lordship of Christ. Education should cultivate knowledge, spiritual maturity, and responsible freedom shaped by Scripture and the purpose of the school."),
    ("XIII. Stewardship", "Everything belongs to God, and Christians are entrusted with time, abilities, and possessions. They should use these gifts generously, regularly, and wisely for God's glory and the good of others."),
    ("XIV. Cooperation", "Churches and Christian organizations may voluntarily cooperate for missions, education, benevolence, and other kingdom purposes. Such cooperation is advisory and must not replace the authority or conscience of the local church."),
    ("XV. The Christian and the Social Order", "Christians should pursue righteousness, truth, compassion, and the good of their neighbors. Social action should flow from the gospel, uphold human dignity, care for the vulnerable, and remain loyal to Christ."),
    ("XVI. Peace and War", "Christians should pursue peace and oppose the spirit of war through righteous action, prayer, and the reconciling message of the gospel of Jesus Christ."),
    ("XVII. Religious Liberty", "God alone is Lord of the conscience. Churches and the state should remain institutionally separate, while every person is protected in the freedom to seek, hold, and share religious convictions without coercion."),
    ("XVIII. The Family", "God designed the family as a foundational institution of society. Marriage, parenting, and family life should reflect God's purposes, honor the equal dignity of each person, and teach children to live by biblical truth."),
)

BFM_ARTICLES_ES = (
    ("I. Las Escrituras", "La Biblia es la revelación confiable de Dios y la norma suprema para la fe, la unidad cristiana y la conducta humana. Nos dirige a Cristo y nos enseña cómo Dios juzga y salva."),
    ("II. Dios", "Hay un solo Dios verdadero, santo, personal y soberano, quien creó y sostiene todas las cosas. Se ha revelado como Padre, Hijo y Espíritu Santo, distintos en persona y unidos en naturaleza divina."),
    ("III. El Ser Humano", "Los seres humanos fueron creados a imagen de Dios como hombre y mujer, con dignidad y responsabilidad. El pecado ha afectado a toda persona, y solo la gracia de Dios puede restaurarnos a la comunión con él."),
    ("IV. La Salvación", "La salvación se ofrece gratuitamente por medio de Jesucristo e incluye a la persona completa. La obra salvadora de Dios incluye el nuevo nacimiento, la justificación, la santificación y la glorificación final, y se recibe mediante la fe personal en Cristo."),
    ("V. El Propósito de Gracia de Dios", "Dios salva y guarda a su pueblo por gracia, cumpliendo sus propósitos sin negar la responsabilidad humana. Su gracia excluye la jactancia, produce humildad y permite que los creyentes perseveren en la fe."),
    ("VI. La Iglesia", "Una iglesia local es una comunidad de creyentes bautizados, unidos por pacto bajo el señorío de Cristo, reunidos para adorar, hacer discípulos, cumplir la misión y rendirse cuentas mutuamente. Sus oficios bíblicos son pastor o anciano y diácono."),
    ("VII. El Bautismo y la Cena del Señor", "El bautismo y la Cena del Señor son las ordenanzas de la iglesia. El bautismo representa la unión del creyente con Cristo en su muerte y resurrección, mientras que la Cena recuerda la muerte de Cristo y anticipa su regreso."),
    ("VIII. El Día del Señor", "El primer día de la semana se aparta para la adoración cristiana y la devoción espiritual en memoria de la resurrección de Jesús. Su observancia debe ser guiada por la conciencia bajo el señorío de Cristo."),
    ("IX. El Reino", "Dios reina sobre toda la creación, y su reinado salvador se recibe mediante la confianza humilde en Jesucristo. Los cristianos oran y trabajan para que se haga la voluntad de Dios mientras esperan la consumación final del reino."),
    ("X. Las Últimas Cosas", "Dios llevará la historia a su final señalado. Cristo regresará visiblemente, resucitará a los muertos y juzgará a todos; los redimidos vivirán con él, mientras los injustos enfrentarán castigo eterno."),
    ("XI. El Evangelismo y las Misiones", "Cada cristiano y cada iglesia comparte el privilegio y el deber de hacer discípulos entre todos los pueblos. La proclamación del evangelio debe estar respaldada por una vida que refleje el mensaje de Cristo."),
    ("XII. La Educación", "La educación cristiana busca la sabiduría bajo el señorío de Cristo. Debe cultivar el conocimiento, la madurez espiritual y una libertad responsable, guiada por las Escrituras y el propósito de la institución."),
    ("XIII. La Mayordomía", "Todo pertenece a Dios, y los cristianos reciben en confianza su tiempo, capacidades y posesiones. Deben usar estos dones con generosidad, regularidad y sabiduría para la gloria de Dios y el bien de los demás."),
    ("XIV. La Cooperación", "Las iglesias y organizaciones cristianas pueden cooperar voluntariamente para las misiones, la educación, la benevolencia y otros propósitos del reino. Esta cooperación es aconsejable y no debe reemplazar la autoridad ni la conciencia de la iglesia local."),
    ("XV. El Cristiano y el Orden Social", "Los cristianos deben buscar la justicia, la verdad, la compasión y el bien de sus vecinos. La acción social debe fluir del evangelio, afirmar la dignidad humana, cuidar a los vulnerables y permanecer fiel a Cristo."),
    ("XVI. La Paz y la Guerra", "Los cristianos deben buscar la paz y oponerse al espíritu de guerra mediante acciones justas, oración y el mensaje reconciliador del evangelio de Jesucristo."),
    ("XVII. La Libertad Religiosa", "Solo Dios es Señor de la conciencia. La iglesia y el Estado deben permanecer separados institucionalmente, mientras toda persona es protegida en su libertad de buscar, sostener y compartir sus convicciones religiosas sin coerción."),
    ("XVIII. La Familia", "Dios diseñó la familia como una institución fundamental de la sociedad. El matrimonio, la crianza y la vida familiar deben reflejar los propósitos de Dios, honrar la dignidad igual de cada persona y enseñar a los hijos a vivir conforme a la verdad bíblica."),
)


BELIEF_PAGES = {
    "nicene-creed": {
        "title": "Nicene Creed",
        "title_es": "Credo Niceno",
        "description": (
            "Read the Nicene Creed and learn how Sojourn Church confesses the historic "
            "Christian faith concerning the Father, Son, and Holy Spirit."
        ),
        "description_es": (
            "Lee el Credo Niceno y conoce cómo Iglesia Sojourn confiesa la fe cristiana "
            "histórica acerca del Padre, el Hijo y el Espíritu Santo."
        ),
        "intro": (
            "The Nicene Creed is a historic summary of the Christian faith and a confession "
            "of the church's unity across generations and places."
        ),
        "intro_es": (
            "El Credo Niceno es un resumen histórico de la fe cristiana y una confesión de "
            "la unidad de la iglesia a través de generaciones y lugares."
        ),
        "body": (
            "We believe in one God, the Father almighty, maker of heaven and earth, of all "
            "things visible and invisible.\n\n"
            "We believe in one Lord Jesus Christ, the only Son of God, begotten from the "
            "Father before all ages, God from God, Light from Light, true God from true God, "
            "begotten, not made; of the same essence as the Father. Through him all things were "
            "made. For us and for our salvation he came down from heaven; he became incarnate "
            "by the Holy Spirit and the virgin Mary, and was made human. He was crucified for "
            "us under Pontius Pilate; he suffered and was buried. The third day he rose again, "
            "according to the Scriptures. He ascended to heaven and is seated at the right hand "
            "of the Father. He will come again with glory to judge the living and the dead. His "
            "kingdom will have no end.\n\n"
            "We believe in the Holy Spirit, the Lord, the giver of life. He proceeds from the "
            "Father and the Son, and with the Father and the Son is worshiped and glorified. He "
            "spoke through the prophets. We believe in one holy catholic and apostolic church. "
            "We affirm one baptism for the forgiveness of sins. We look forward to the resurrection "
            "of the dead, and to life in the world to come. Amen."
        ),
        "body_es": (
            "Creemos en un solo Dios, Padre todopoderoso, creador del cielo y de la tierra, "
            "de todo lo visible y lo invisible.\n\n"
            "Creemos en un solo Señor, Jesucristo, Hijo único de Dios, nacido del Padre antes "
            "de todos los siglos: Dios de Dios, Luz de Luz, Dios verdadero de Dios verdadero, "
            "engendrado, no creado, de la misma naturaleza del Padre. Por quien todo fue hecho. "
            "Que por nosotros y por nuestra salvación bajó del cielo; por obra del Espíritu Santo "
            "se encarnó de María, la Virgen, y se hizo hombre. Por nuestra causa fue crucificado "
            "en tiempos de Poncio Pilato; padeció y fue sepultado. Resucitó al tercer día, según "
            "las Escrituras. Subió al cielo y está sentado a la derecha del Padre. De nuevo vendrá "
            "con gloria para juzgar a vivos y muertos, y su reino no tendrá fin.\n\n"
            "Creemos en el Espíritu Santo, Señor y dador de vida, que procede del Padre y del Hijo, "
            "que con el Padre y el Hijo recibe una misma adoración y gloria, y que habló por los "
            "profetas. Creemos en la Iglesia, que es una, santa, católica y apostólica. Confesamos "
            "un solo bautismo para el perdón de los pecados. Esperamos la resurrección de los "
            "muertos y la vida del mundo futuro. Amén."
        ),
        "article_headings": ("The Father", "The Son", "The Holy Spirit"),
        "article_headings_es": ("El Padre", "El Hijo", "El Espíritu Santo"),
        "continuous": True,
        "source": "A historic Christian creed; wording adapted from the 2013 English translation.",
        "source_es": "Un credo cristiano histórico; texto adaptado de la traducción inglesa de 2013.",
    },
    "apostles-creed": {
        "title": "Apostles' Creed",
        "title_es": "Credo de los Apóstoles",
        "description": (
            "Read the Apostles' Creed, a historic summary of the Christian faith confessed by "
            "Sojourn Church."
        ),
        "description_es": (
            "Lee el Credo de los Apóstoles, un resumen histórico de la fe cristiana que confiesa "
            "Iglesia Sojourn."
        ),
        "intro": (
            "The Apostles' Creed is a concise confession of the faith Christians have shared "
            "across the centuries."
        ),
        "intro_es": (
            "El Credo de los Apóstoles es una confesión concisa de la fe que los cristianos han "
            "compartido a través de los siglos."
        ),
        "body": (
            "I believe in God, the Father almighty, Creator of heaven and earth.\n\n"
            "I believe in Jesus Christ, his only Son, our Lord, who was conceived by the Holy "
            "Spirit, born of the virgin Mary, suffered under Pontius Pilate, was crucified, died, "
            "and was buried; he descended to the dead. The third day he rose again from the dead. "
            "He ascended to heaven and is seated at the right hand of God the Father almighty. From "
            "there he will come to judge the living and the dead.\n\n"
            "I believe in the Holy Spirit, the holy catholic church, the communion of saints, the "
            "forgiveness of sins, the resurrection of the body, and the life everlasting. Amen."
        ),
        "body_es": (
            "Creo en Dios Padre todopoderoso, creador del cielo y de la tierra.\n\n"
            "Creo en Jesucristo, su único Hijo, nuestro Señor, que fue concebido por obra del "
            "Espíritu Santo, nació de la virgen María, padeció bajo el poder de Poncio Pilato, fue "
            "crucificado, muerto y sepultado; descendió a los muertos. Al tercer día resucitó de "
            "entre los muertos. Subió al cielo y está sentado a la derecha de Dios Padre "
            "todopoderoso. Desde allí vendrá a juzgar a vivos y muertos.\n\n"
            "Creo en el Espíritu Santo, la santa iglesia católica, la comunión de los santos, el "
            "perdón de los pecados, la resurrección del cuerpo y la vida eterna. Amén."
        ),
        "article_headings": ("The Father", "Jesus Christ", "The Holy Spirit"),
        "article_headings_es": ("El Padre", "Jesucristo", "El Espíritu Santo"),
        "continuous": True,
        "source": "A historic Christian creed; wording adapted from the 1979 Book of Common Prayer.",
        "source_es": "Un credo cristiano histórico; texto adaptado del Libro de Oración Común de 1979.",
    },
    "baptist-faith-and-message-2000": {
        "title": "Baptist Faith and Message 2000",
        "title_es": "Fe y Mensaje Bautistas 2000",
        "description": (
            "Learn why Sojourn Church identifies with the Baptist Faith and Message 2000 and "
            "visit the official statement of faith."
        ),
        "description_es": (
            "Conoce por qué Iglesia Sojourn se identifica con Fe y Mensaje Bautistas 2000 y "
            "visita la declaración oficial de fe."
        ),
        "intro": (
            "Sojourn Church affirms the Baptist Faith and Message 2000 as one of the documents "
            "that describes our theological convictions. It is read alongside the historic creeds "
            "and the New Hampshire Confession of Faith."
        ),
        "intro_es": (
            "Iglesia Sojourn afirma Fe y Mensaje Bautistas 2000 como uno de los documentos que "
            "describe nuestras convicciones teológicas. Lo leemos junto con los credos históricos "
            "y la Confesión de Fe de New Hampshire."
        ),
        "body": (
            "The Baptist Faith and Message 2000 addresses the Scriptures, God, humanity, salvation, "
            "God's purpose of grace, the church, baptism and the Lord's Supper, the Lord's Day, the "
            "kingdom, last things, evangelism and missions, education, stewardship, cooperation, the "
            "Christian and the social order, peace and war, religious liberty, and the family."
        ),
        "body_es": (
            "Fe y Mensaje Bautistas 2000 aborda las Escrituras, Dios, la humanidad, la salvación, "
            "el propósito de gracia de Dios, la iglesia, el bautismo y la Cena del Señor, el Día del "
            "Señor, el reino, las últimas cosas, el evangelismo y las misiones, la educación, la "
            "mayordomía, la cooperación, el cristiano y el orden social, la paz y la guerra, la "
            "libertad religiosa y la familia."
        ),
        "articles": BFM_ARTICLES,
        "articles_es": BFM_ARTICLES_ES,
        "source": (
            "This page provides Sojourn's original overview of all 18 articles. "
            "Because the official statement is maintained by the Southern Baptist Convention, "
            "we link to the current official text rather than reproducing it here."
        ),
        "source_es": (
            "Esta página ofrece un resumen original de Sojourn sobre los 18 artículos. "
            "Como la Convención Bautista del Sur mantiene la declaración oficial, enlazamos "
            "al texto oficial vigente en lugar de reproducirlo aquí."
        ),
        "source_url": BFM_SOURCE_URL,
        "source_url_es": BFM_SOURCE_ES_URL,
    },
    "new-hampshire-confession-of-faith": {
        "title": "New Hampshire Confession of Faith",
        "title_es": "Confesión de Fe de New Hampshire",
        "description": "Read the 1853 New Hampshire Confession of Faith, a historic Baptist confession that helps shape Sojourn Church's teaching.",
        "description_es": "Lee la Confesión de Fe de New Hampshire de 1853, una confesión bautista histórica que forma la enseñanza de Iglesia Sojourn.",
        "intro": "This historic Baptist confession helps explain the theological tradition shaping Sojourn Church's teaching.",
        "intro_es": "Esta confesión bautista histórica ayuda a explicar la tradición teológica que forma la enseñanza de Iglesia Sojourn.",
        "body": "",
        "body_es": "",
        "source": "This page follows the 1853 transcription published by Grace Baptist Church, Cape Coral.",
        "source_es": "Esta página sigue la transcripción de 1853 publicada por Grace Baptist Church de Cape Coral.",
        "source_url": CONFESSION_SOURCE_URL,
    },
}


BELIEF_SUMMARIES = (
    {
        "slug": "nicene-creed",
        "title": "Nicene Creed",
        "title_es": "Credo Niceno",
        "summary": "A historic confession of the triune God, Jesus Christ, the Holy Spirit, the church, and the hope of resurrection.",
        "summary_es": "Una confesión histórica del Dios trino, Jesucristo, el Espíritu Santo, la iglesia y la esperanza de la resurrección.",
    },
    {
        "slug": "apostles-creed",
        "title": "Apostles' Creed",
        "title_es": "Credo de los Apóstoles",
        "summary": "A concise statement of the Christian faith centered on the Father, Son, Holy Spirit, forgiveness, resurrection, and eternal life.",
        "summary_es": "Una declaración concisa de la fe cristiana centrada en el Padre, el Hijo, el Espíritu Santo, el perdón, la resurrección y la vida eterna.",
    },
    {
        "slug": "baptist-faith-and-message-2000",
        "title": "Baptist Faith and Message 2000",
        "title_es": "Fe y Mensaje Bautistas 2000",
        "summary": "A contemporary Baptist statement addressing Scripture, salvation, the church, mission, religious liberty, and the family.",
        "summary_es": "Una declaración bautista contemporánea sobre las Escrituras, la salvación, la iglesia, la misión, la libertad religiosa y la familia.",
    },
    {
        "slug": "new-hampshire-confession-of-faith",
        "title": "New Hampshire Confession of Faith",
        "title_es": "Confesión de Fe de New Hampshire",
        "summary": "A historic Baptist confession that helps explain the theological tradition shaping Sojourn Church's teaching.",
        "summary_es": "Una confesión bautista histórica que ayuda a explicar la tradición teológica que forma la enseñanza de Iglesia Sojourn.",
    },
)


def get_belief_page(slug, language="en"):
    """Return a localized dedicated belief page payload."""
    language = (language or "en").split("-")[0]
    page = BELIEF_PAGES[slug].copy()
    suffix = "_es" if language == "es" else ""
    for key in ("title", "description", "intro", "body", "source"):
        page[key] = page[f"{key}{suffix}"]
    page["paragraphs"] = [paragraph for paragraph in page["body"].split("\n\n") if paragraph]
    if language == "es" and page.get("source_url_es"):
        page["source_url"] = page["source_url_es"]
    localized_articles = page.get("articles_es" if language == "es" else "articles")
    if localized_articles:
        page["articles"] = localized_articles
    headings = page.get("article_headings_es" if language == "es" else "article_headings")
    if headings:
        page["articles"] = tuple(zip(headings, page["paragraphs"]))
    page["slug"] = slug
    if slug == "new-hampshire-confession-of-faith":
        page["title"] = "Confesión de Fe de New Hampshire" if language == "es" else "New Hampshire Confession of Faith"
        page["description"] = (
            "Lee la Confesión de Fe de New Hampshire de 1853, una confesión bautista histórica que forma la enseñanza de Iglesia Sojourn."
            if language == "es"
            else "Read the 1853 New Hampshire Confession of Faith, a historic Baptist confession that helps shape Sojourn Church's teaching."
        )
        page["intro"] = (
            "Esta confesión bautista histórica ayuda a explicar la tradición teológica que forma la enseñanza de Iglesia Sojourn."
            if language == "es"
            else "This historic Baptist confession helps explain the theological tradition shaping Sojourn Church's teaching."
        )
        page["articles"] = get_confession_articles(language)
        page["source"] = (
            "Esta página sigue la transcripción de 1853 publicada por Grace Baptist Church de Cape Coral."
            if language == "es"
            else "This page follows the 1853 transcription published by Grace Baptist Church, Cape Coral."
        )
        page["source_url"] = CONFESSION_SOURCE_URL
    return page
