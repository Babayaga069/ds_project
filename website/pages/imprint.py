import dash
from dash import html

dash.register_page(__name__, path="/imprint", name="Imprint")


layout = html.Div([
    html.H1("Impressum"),

    html.H2("Anschrift:"),
    html.P([
        "Christian-Albrechts-Universität zu Kiel", html.Br(),
        "Christian-Albrechts-Platz 4", html.Br(),
        "24118 Kiel, Germany", html.Br(),
        "Telefon: +49 (0431) 880-00", html.Br(),
        "E-Mail: mail@uni-kiel.de"
    ]),

    html.H2("Gesetzliche Vertretung:"),
    html.P(
        "Die Christian-Albrechts-Universität zu Kiel ist eine Körperschaft des Öffentlichen Rechts. "
        "Sie wird gesetzlich durch das Präsidium vertreten."
    ),

    html.H2("Zuständige Aufsichtsbehörde:"),
    html.P([
        "Ministerium für Allgemeine und Berufliche Bildung, Wissenschaft, Forschung und Kultur (MBWFK)", html.Br(),
        "Brunswiker Straße 16-22", html.Br(),
        "24105 Kiel"
    ]),

    html.H2("Umsatzsteueridentifikationsnummer:"),
    html.P("DE 811317279"),

    html.H2("Verantwortlich im Sinne des Pressegesetzes:"),
    html.P("Das Präsidium"),

    html.H2("Technische Betreuung:"),
    html.P([
        "Rechenzentrum (RZ) der CAU", html.Br(),
        "E-Mail: websupport@rz.uni-kiel.de"
    ]),

    html.H1("Erklärung zur Barrierefreiheit"),

    html.P(
        "Die Christian-Albrechts-Universität zu Kiel (CAU) ist bemüht, ihren Webauftritt im Einklang "
        "mit den nationalen Rechtsvorschriften zur Umsetzung der Richtlinie (EU) 2016/2102 des "
        "Europäischen Parlaments und des Rates barrierefrei zugänglich zu machen."
    ),

    html.P(
        "Diese Erklärung zur Barrierefreiheit gilt für den Webauftritt der CAU bzw. für die Inhalte, "
        "die über die von der Universität zentral zur Verfügung gestellten Web Content-Management-Systeme "
        "(WCMS) erreichbar sind (www.uni-kiel.de sowie entsprechende Sub-Domains)."
    ),

    html.H2("Stand der Vereinbarkeit mit den Anforderungen"),
    html.P(
        "Der Webauftritt ist teilweise mit § 11 Absatz 1 Landesbehindertengleichstellungsgesetz (LBGG) "
        "sowie den Anforderungen der Barrierefreiheit gemäß § 13 Absatz 3 LBGG vereinbar."
    ),

    html.H2("Nicht barrierefreie Inhalte"),
    html.Ul([
        html.Li(
            "PDF-Downloads: Aufgrund der großen Anzahl der Dokumente konnten diese bislang nicht in ein "
            "barrierefreies Format überführt werden. Sofern sie für aktive Verwaltungsverfahren notwendig "
            "sind, werden diese schrittweise barrierefrei überarbeitet."
        ),
        html.Li(
            "Untertitel: Eingebundene Videos verfügen nicht immer über auslesbare Untertitel. Bei neuen, "
            "eingebundenen Videos, die von uns selbst produziert wurden, sind wir bemüht, Untertitel "
            "schnellstmöglich nach der Veröffentlichung nachzureichen. Der Hinweis auf die Notwendigkeit "
            "der Bereitstellung auslesbarer Untertitel ist fester Bestandteil unseres Schulungskonzepts "
            "für neue Redaktionsmitglieder."
        ),
        html.Li(
            "Alternativtexte: Nicht alle eingesetzten Bilder verfügen über einen Alternativtext. "
            "Das Setzen von sinnvollen Alternativtexten ist fester Bestandteil unseres "
            "Schulungskonzepts für neue Redaktionsmitglieder."
        ),
        html.Li(
            "Überschriften: Nicht alle Seiten haben sinnvoll und semantisch korrekt gesetzte Überschriften. "
            "Das semantisch korrekte Auszeichnen von Überschriftenhierarchien ist fester Bestandteil "
            "unseres Schulungskonzepts für neue Redaktionsmitglieder."
        ),
        html.Li(
            "Sonderzeichen: Auf einzelnen Webseiten werden in den Texten Sonderzeichen genutzt, um den "
            "Bedarfen einer diversitätssensiblen Sprache gerecht zu werden. Die Verwendung von "
            "Sonderzeichen in Texten kann für verschiedene Bedarfsgruppen eine Barriere darstellen. "
            "Wir verfolgen die Diskussion um die Vereinbarkeit des Einsatzes von Sonderzeichen im Rahmen "
            "einer diversitätssensiblen Sprache und den Anforderungen an die Barrierefreiheit aufmerksam."
        ),
        html.Li(
            "Tabellen: Nicht alle eingesetzten Tabellen sind korrekt ausgezeichnet. Das korrekte "
            "Auszeichnen sowie der korrekte Einsatz von Tabellen ist fester Bestandteil unseres "
            "Schulungskonzepts für neue Redaktionsmitglieder."
        ),
        html.Li(
            "Gleichlautende Links: Auf einzelnen Webseiten können gleichlautende Links stehen. Dies ist "
            "teilweise der automatischen Erstellung dieser Links geschuldet. Auch bei redaktionell "
            "gesetzten Links sind gleichlautende Links auf einer Seite nicht immer vermeidbar. In diesen "
            "Fällen bemühen wir uns jedoch, eine entsprechend auslesbare Alternativinformation "
            "bereitzustellen. Der Hinweis auf die Notwendigkeit sprechender Links im Sinne der "
            "Barrierefreiheit ist fester Bestandteil unseres Schulungskonzepts für neue Redaktionsmitglieder."
        ),
        html.Li(
            "Kontraste: Nicht alle Teilbereiche unseres Webauftritts erfüllen die Mindestanforderungen "
            "an Kontraste, z.B. einige Farbkombinationen bei Überschriften und Hintergründen. Wir achten "
            "bei der Neukonzipierung einzelner Teilbereiche explizit auf eine Vereinbarkeit der "
            "Kontrastwerte mit den Mindestanforderungen."
        ),
        html.Li(
            "Tastaturbedienbarkeit: Nicht alle Teilbereiche unseres Webauftritts sind vollständig per "
            "Tastatur zu bedienen, teilweise entspricht die Größe des Fokusfeldes z.B. nicht den "
            "Mindestanforderungen. Dies betrifft vor allem sehr alte Teilbereiche unseres Webauftritts. "
            "Nach der Neukonzipierung einzelner Teilbereiche sind diese Mängel für diese Teilbereiche "
            "abgestellt."
        ),
    ]),

    html.P(
        "Der Webauftritt der CAU ist sehr umfangreich und wird redaktionell in den meisten Fällen "
        "dezentral betreut. Die Sensibilisierung der Redaktionsmitglieder für das Erstellen "
        "barrierearmer Webseiten ist eine Daueraufgabe, die z.B. im Rahmen unseres Schulungskonzeptes "
        "aktiv betrieben wird."
    ),

    html.H2("Erstellung dieser Erklärung zur Barrierefreiheit"),
    html.P("Diese Erklärung wurde erstmalig am 22. September 2022 erstellt."),
    html.P(
        "Die Aussagen bezüglich der Vereinbarkeit mit den Barrierefreiheitsanforderungen in dieser "
        "Erklärung beruhen auf einer Selbstbewertung."
    ),
    html.P("Die Erklärung wurde zuletzt am 23. Dezember 2025 überprüft und aktualisiert."),

    html.H2("Barriere melden! Feedback zur Barrierefreiheit"),
    html.P(
        "Sind Ihnen Mängel beim barrierefreien Zugang zu Inhalten von www.uni-kiel.de aufgefallen? "
        "Dann können Sie sich gerne bei uns melden und Ihr Feedback an uns senden."
    ),

    html.H2("Beschwerdestelle für barrierefreie Informationstechnik Schleswig-Holstein"),
    html.P(
        "Bei der Landesbeauftragten für Menschen mit Behinderung gibt es eine Beschwerdestelle gemäß § 12 LBGG. "
        "Die Beschwerdestelle hat die Aufgabe, Konflikte zwischen Menschen mit Behinderungen und öffentlichen "
        "Stellen des Landes zu lösen. Sie können die Beschwerdestelle einschalten, wenn Sie mit den Antworten "
        "aus der oben genannten Kontaktmöglichkeit nicht zufrieden sind. Dabei geht es nicht darum, Gewinner "
        "oder Verlierer zu finden. Vielmehr ist es das Ziel, mit Hilfe der Beschwerdestelle gemeinsam und "
        "außergerichtlich eine Lösung für ein Problem zu finden. Das Beschwerdeverfahren ist kostenlos. "
        "Sie brauchen auch keinen Rechtsbeistand. Auf der Internetseite der Beschwerdestelle finden Sie alle "
        "Informationen zum Beschwerdeverfahren. Dort können Sie nachlesen, wie ein Beschwerdeverfahren abläuft."
    ),

    html.H2("Sie erreichen die Beschwerdestelle unter folgender Adresse:"),
    html.P("Beschwerdestelle nach dem Behindertengleichstellungsgesetz bei der Landesbeauftragten für Menschen mit Behinderung"),

    html.H3("Büroanschrift:"),
    html.P([
        "Karolinenweg 1", html.Br(),
        "24105 Kiel", html.Br(),
        "Beschwerde: +49 (0431) 988-1620", html.Br(),
        "Beschwerde: bbit@landtag.ltsh.de"
    ])
], style={
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "40px",
    "lineHeight": "1.6"
})