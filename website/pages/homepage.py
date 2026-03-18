import dash
from dash import html, dcc

dash.register_page(__name__, name="Home")

layout = html.Div([
    html.H1("Movie Data Science Project"),
    
    html.H2("Summary"),
    html.P(
        "Movies are a major part of popular culture, and understanding what drives their success is both interesting and challenging. "
        "In this project, we explore factors influencing financial and critical outcomes of films, including production budgets, genres, release years, "
        "directors, and audience engagement. Using different comprehensive and freely accessible movie APIs, we collected large-scale data to "
        "analyze trends across decades and genres. The questions we tackle cover everything from box office predictions and genre trends to director influence, "
        "actor collaborations, sequel performance, award impact, and the role of pre-release public interest. This study provides both quantitative insights "
        "and visualizations to better understand patterns in movie success."
    ),
    
    html.H2("Questions"),
    html.Ol([
        html.Li("How strongly does production budget predict box office revenue across different genres and release periods?"),
        html.Li("Which combination of production studio, genre, runtime and release year best explains rating-based movie success for anime movies in the last 26 years?"),
        html.Li("What are trends in the movie industry in terms of genre distribution and box office revenue from 2000 to 2025?"),
        html.Li("How does the historical success over the last 30-40 years of the 10 most popular active directors influence the financial and critical success of their new movie releases?"),
        html.Li("How does the financial and critical success of movie sequels between 2010 and 2024 compare to their original films across franchises?"),
        html.Li("How does film genre, along with production budget, influence the likelihood of receiving an Academy Award nomination?"),
        html.Li("How does receiving an Academy Award nomination or win influence a film’s box office revenue?"),
        html.Li("How does pre- and post-release Google search interest relate to the financial and critical success of movies released between 2010 and 2024?"),
        html.Li("How does sticking to typical genre plots lead to greater box office success for fantasy and horror movies (from 2000 to 2025)?")
    ]),
    
    html.H2("About us"),
    html.P(
        "This project is part of a Data Science study carried out by a team of 4 members who share a passion for movies. "
        "We used APIs such as TMDB to collect large-scale data efficiently and analyzed it using Python and data science tools. "
        "Our goal was to answer the research questions systematically, combining statistical analysis with visualizations. "
        "The results provide insights into financial and critical movie success, genre trends, director and actor influence, sequel performance, and audience engagement."
    )
])