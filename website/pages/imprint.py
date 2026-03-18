import dash
from dash import html

dash.register_page(__name__, path="/imprint", name="Imprint")


layout = html.Div([
    html.H1("Imprint"),

    html.H2("Address"),
    html.P([
        "Christian-Albrechts-University of Kiel", html.Br(),
        "Christian-Albrechts-Platz 4", html.Br(),
        "24118 Kiel, Germany", html.Br(), html.Br(),
        "Phone: +49 (0431) 880-00", html.Br(),
        "Email: mail@uni-kiel.de"
    ]),
    
], style={
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "40px",
    "lineHeight": "1.6"
})