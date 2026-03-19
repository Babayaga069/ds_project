import dash
from dash import html, dcc, callback, Input, Output
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
import ast

# register as new page
dash.register_page(__name__, name="Question: 2", order=2)

csv = pd.read_csv('pages\q2\details_anime_movies_2000.csv')

# helper function
def exploding_genre(data):
    data = data.copy()
    # converting string of a list into literal list
    data['genres'] = data['genres'].apply(ast.literal_eval)

    # filtering out the genre animation, due to all movies being animation movies
    data['genres'] = data['genres'].apply(lambda g: [x for x in g if x != "Animation" and x != "TV Movie"])
    
    # breaking up genre animation, due to all movies being animation movies
    genres = data['genres'].explode()

    # assigning values to each genre to quantify them
    genre_dummies = pd.get_dummies(genres)
    genre_dummies = genre_dummies.groupby(level=0).sum()

    return genre_dummies

def exploding_studio(data, studio_amount = 10):
    data = data.copy()
    # converting string of a list into literal list
    data['production_studios'] = data['production_studios'].apply(ast.literal_eval)

    # breaking up production companios to get single categories
    studios = data['production_studios'].explode()

    # only showing the chosen amount of most frequent production studios
    top_studios = studios.value_counts().head(studio_amount).index
    return top_studios

def loading_data(data,studio_amount = 10):
    data.copy()
    genre_dummies = exploding_genre(data)
    data = pd.concat([data, genre_dummies], axis=1)

    top_studios = exploding_studio(data, studio_amount)


    for studio in top_studios:
        data[studio] = data["production_studios"].apply(lambda x: int(studio in x))

    y = data['avg_score']

    X = data[
        ["runtime", "release_year"] +
        list(genre_dummies.columns) +
        list(top_studios)
    ]
    X = np.array(X)
    y = np.array(y)

    X = np.c_[np.ones(X.shape[0]), X] # add intercept

    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    features = ['intercept', 'runtime', 'release_year'] + list(genre_dummies.columns) + list(top_studios)

    coeff_data = pd.DataFrame({
        'feature' : features,
        'coefficient' : beta
    })


    #print(coeff_data.sort_values('coefficient',ascending=False))

    return data

def runtime_scatter_plot(csv):
    data = loading_data(csv)
    fig = px.scatter(data, x='runtime', y='avg_score',
                     title='Ratings across Runtimes ')
    return fig

def genre_bar_chart_rating(csv):
    data = loading_data(csv)
    genre_dummies = exploding_genre(csv.copy())

    genre_means = {}
    for g in genre_dummies.columns:
    
        genre_means[g] = data[data[g] == 1]['avg_score'].mean()
    
    genre_series = pd.Series(genre_means).sort_values().reset_index()
    genre_series.columns= ['genres','avg_score']
    fig = px.bar(
        genre_series,
        x='genres',
        y='avg_score',
        title='Average Ratings by Genres',
        labels={'genres': 'Genre', 'avg_score': 'Average Rating'}
    )

    return fig

def ratings_over_time_plot(csv):
    data = loading_data(csv)
    year_means = data.groupby('release_year')["avg_score"].mean().reset_index()

    fig = px.line(
        year_means,
        x='release_year',
        y='avg_score',
        title='Ratings across Release Years',
        labels={
            'release_year' : 'Release Year',
            'avg_score' : 'Average Rating'
        }
    )
    return fig

def ratings_over_top_studios(csv, studios_amount = 10):
    data = loading_data(csv,studios_amount)

    studio_scores = {}

    top_studios = exploding_studio(csv, studios_amount)
    for s in top_studios:
        studio_scores[s] = data[data[s] == 1]['avg_score'].mean()

    studio_series = pd.Series(studio_scores).sort_values(ascending=True).head(studios_amount).reset_index()
    studio_series.columns = ['production_studios', 'avg_score']

    fig = px.bar(
        studio_series,
        x='production_studios',
        y='avg_score',
        title='Average Scores across Production Studios',
        labels={
            'production_studios': 'Production Studios',
            'avg_score': 'Average Rating'
        }
    )
    return fig



runtime_ratings = runtime_scatter_plot(csv)
genre_ratings = genre_bar_chart_rating(csv)
release_year_ratings= ratings_over_time_plot(csv)
studio_ratings = ratings_over_top_studios(csv)    

# LAYOUT:
layout = html.Div([

    html.H1("Which combination of production studio, genre, runtime and release year best explains rating-based movie success  for anime movies in the last 26 years?"),
    html.H2("Context"),
    html.P("This analysis explores the key factors that influence the critical success of anime movies over the past 26 years." \
            "We used an average rating per movie, consisting of Metacritic, Rotten Tomatoes, IMDb and TMDb scores (as available), as a measure of critical success. " \
            "By examining trends across production studios, release years, runtimes, and genres, the goal is to identify patterns that explain why certain movies perform better than others."),
    html.H2("Ratings across Ratings and Release Years"),

    html.Div([
        dcc.Graph(figure=runtime_ratings, style={'width': '50%'}),
        dcc.Graph(figure=release_year_ratings, style={'width': '50%'})
    ], style={'display': 'flex', 'gap':'20px'}),

    html.Div([
        dcc.Graph(figure=genre_ratings)
    ], style={'width': '100%', 'display' :'inline-block'}),

    html.H2("Ratings across Production Studios and Genres"),
    html.Div([
        html.H3("Top Studio Ratings"),
        html.P('The Studios are sorted by the amount of Anime Movies they have worked in. The higher the slider, the less known the studios shown.'), 
        dcc.Slider(
            id='studio-slider',
            min=0,
            max=50,
            step=1,
            value=10,
            marks={i: str(i) for i in range(0, 50, 5)},
        ),
        dcc.Graph(id='studio-bar-chart')
    ]),

    html.H1("Take Away"),
    html.P("The data suggests that higher-rated anime movies are most strongly associated with recent release years.\
            Further emotionally driven genres like drama, music and romance perform better than spectacular genres, like action, adventure or horror movies, \
            while runtimes mostly cluster around 100–120 minutes and exceptions having higher variability with higher and lower ratings with shorter or longer runtimes.\
            The top production studios further enhance overall quality, with most of the studios that have lots of titles, also performing better.")
])

# CALLBACKS


@callback(
    Output('studio-bar-chart', 'figure'),
    Input('studio-slider', 'value')
)
def update_chart(studios_amount):
    if not studios_amount:
        return {}
    return ratings_over_top_studios(csv, studios_amount)



