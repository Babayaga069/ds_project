import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import plotly.express as px

dash.register_page(__name__, name='Data')

layout=html.Div([

  html.H2("Credits"),
    # Hier fehlen auf dem Screenshot die eckigen Klammern nach der runden Klammer!
    html.P([
        "This product uses the ",
        html.A("TMDB API", href="https://www.themoviedb.org/", target="_blank"),
        " but is not endorsed or certified by TMDB."
    ]),
    html.Div([
        html.A(
            # Das Logo-Bild
            html.Img(
                # Link zum offiziellen TMDB-Logo (SVG ist am besten für Skalierbarkeit)
                src="/assets/TMDB_logo.svg",
                alt="TMDB Logo",
                style={'height': '100px', 'margin-right': '10px'} # Größe und Abstand anpassen
            ),
            # Die Ziel-URL für den Link
            href="https://www.themoviedb.org/",
            # WICHTIG: Öffnet den Link in einem neuen Tab
            target="_blank"
        )
    ]),
    html.P([
    "Additional movie Information we got through ",
    html.A("OMDb API", href="https://www.omdbapi.com/", target="_blank"),
    "."
]),





])