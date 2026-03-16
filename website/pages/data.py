import dash 
from dash import html, dcc, callback, Input, Output, State , dash_table
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import plotly.express as px

dash.register_page(__name__, name='Data')
#list made with help of ai
data_entries = [
    {
        "name": "title, original_title, film", 
        "description": "The official title of the movie", 
        "example_value": "The Dark Knight", 
        "source": "TMDB, IMDB, Kaggle"
    },
    {
        "name": "id, tmdb_id, imdb_id", 
        "description": "Unique identifiers used to match movies across databases", 
        "example_value": "tt0313441 / 475762", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "release_date, release_year", 
        "description": "The exact release date or the release year of the movie", 
        "example_value": "2008-07-16 / 2008", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "budget, revenue, box_office", 
        "description": "Financial metrics including production budget and worldwide box office earnings", 
        "example_value": "180,000,000 / 1,067,316,101", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "vote_average, tmdb_rating, imdb_rating", 
        "description": "Average user ratings from the platforms", 
        "example_value": "8.0 / 7.7", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "genres, genre_ids", 
        "description": "The assigned categories or genres of the movie", 
        "example_value": "['Drama', 'Action']", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "overview, plot", 
        "description": "A short summary or plot description of the movie's story", 
        "example_value": "After a great catastrophe...", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "runtime", 
        "description": "The total duration of the movie in minutes", 
        "example_value": "152.0", 
        "source": "TMDB, IMDB"
    },
    {
        "name": "oscar_won, oscar_nominated, category, winner", 
        "description": "Information regarding Oscar nominations, wins, and award categories", 
        "example_value": "True / ACTOR IN A LEADING ROLE", 
        "source": "Kaggle (The Oscar Award)"
    },
    {
        "name": "avg_trend_before, avg_trend_after, roi", 
        "description": "Google Trends search interest averages before/after release and Return on Investment", 
        "example_value": "25.4 / 5.24", 
        "source": "PyTrends"
    }
]
layout=html.Div([
  html.H2("Credits"),
    html.P([
        "Our main data is collected through TMDB. ",
        "This product uses the ",
        html.A("TMDB API", href="https://www.themoviedb.org/", target="_blank"),
        " but is not endorsed or certified by TMDB."
    ]),
    html.Div([
        html.A(
            html.Img(
                src="/assets/TMDB_logo.svg",
                alt="TMDB Logo",
                style={'height': '100px', 'margin-right': '10px'} 
            ),
           
            href="https://www.themoviedb.org/",
            
            target="_blank"
        )
    ]),
    html.P([
    "Additional movie Information we got through ",
    html.A("OMDb API", href="https://www.omdbapi.com/", target="_blank"),
    "."
]),
html.P(["For Data information regarding awards or Oscars we used this ",
        html.A("Kaggle Dataset ", href="https://www.kaggle.com/datasets/unanimad/the-oscar-award?resource=download", target="_blank"),
        "."
]),
html.P(["For Data information regarding Trends and public interest we used ",
        html.A("Pytrends libary", href="https://pypi.org/project/pytrends/", target="_blank"),
        "."
]),
html.H3("Data Overview"), 
dash_table.DataTable(
    data=data_entries,
   
    columns=[
        {"name": "Name", "id": "name"},
        {"name": "Description", "id": "description"},
        {"name": "Example Value", "id": "example_value"},
        {"name": "Source", "id": "source"}
    ],
   style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontFamily': 'Arial, sans-serif',
        'whiteSpace': 'normal', 
        'height': 'auto'        
    },
    
    style_header={
        'backgroundColor': '#f4f4f4', 
        'fontWeight': 'bold',
        'border': '1px solid black'
    },
    style_data={
        'border': '1px solid grey'
    }
)


])