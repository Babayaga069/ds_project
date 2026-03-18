import dash
from dash import html, dcc

dash.register_page(__name__, name="Home")

layout = html.Div([
    html.H1("Movie Data Science Project"),
    
    html.H2("Summary"),
    html.P(
        "We love movies and want to understand what drives their success. "
        "Using TMDB, a large movie database, we can easily collect data "
        "and analyze trends across genres, budgets, directors, and audience reactions."
    ),
    
    html.H2("Questions"),
    html.Ol([
        html.Li("How strongly does production budget predict box office revenue across different genres and release periods?"),
        html.Li("Which combination of production budget, genre, runtime and release year best explains financial and rating-based movie success for anime movies in the last 26 years?"),
        html.Li("What are trends in the movie industry in terms of genre distribution and box office revenue from 2000 to 2025?"),
        html.Li("How does the historical success of directors influence the financial and critical success of new movie releases? (last 30-40 years, 10 most popular active directors)"),
        html.Li("What collaboration networks emerge between actors and directors, and how do recurring collaborations influence movie success?"),
        html.Li("How does the financial and critical success of movie sequels between 2010 and 2024 compare to their original films across franchises?"),
        html.Li("How does film genre, along with production budget, influence the likelihood of receiving an Academy Award nomination?"),
        html.Li("How does receiving an Academy Award nomination or win influence a film’s box office revenue?"),
        html.Li("How does pre- and post-release Google search interest relate to the financial and critical success of movies released between 2010 and 2024?"),
        html.Li("How does sticking to typical genre plots lead to greater box office success for fantasy and horror movies(From 2000 to 2025)")
    ]),
    
    html.H2("about us"),
    html.P(
        "This project is part of a Data Science study conducted by 4 team members. "
        "We analyzed large-scale movie data from TMDB and other sources to answer these questions. "
        "Results include insights on box office performance, audience ratings, director and actor influence, genre trends, and pre-release sentiment."
    )
])