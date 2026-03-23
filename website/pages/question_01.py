import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import numpy as np
import ast
import plotly.express as px

#register as new page
dash.register_page(__name__, name='Question: 1', order=1)

livedata_q1 = pd.read_csv('pages/q1/movies_dataset.csv')


#keep only relevant columns
keep_columns = ["id", "title", "release_date", "budget", "revenue", "genres"]
livedata_q1 = livedata_q1[keep_columns].copy()

#technical cleaning
livedata_q1["release_date"] = pd.to_datetime(livedata_q1["release_date"], errors="coerce")
livedata_q1["release_year"] = livedata_q1["release_date"].dt.year
livedata_q1["budget"] = pd.to_numeric(livedata_q1["budget"], errors="coerce")
livedata_q1["revenue"] = pd.to_numeric(livedata_q1["revenue"], errors="coerce")

#parse stored genre strings safely
livedata_q1["genre_list"] = livedata_q1["genres"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

#create release period categories
period_bins = [1989, 1999, 2009, 2019, 2025]
period_labels = ["1990s", "2000s", "2010s", "2020-2025"]
livedata_q1["release_period"] = pd.cut(
    livedata_q1["release_year"],
    bins=period_bins,
    labels=period_labels
)

#keep only movies with positive budget and revenue
livedata_q1 = livedata_q1[(livedata_q1["budget"] > 0) & (livedata_q1["revenue"] > 0)].copy()

# create log variables
livedata_q1["log_budget"] = np.log(livedata_q1["budget"])
livedata_q1["log_revenue"] = np.log(livedata_q1["revenue"])

#filters dataframe by chosen genre and release period
def filter_data(dataframe, chosen_genre, chosen_period):
    updated_dataframe = dataframe.copy()

    if chosen_genre != "All Genres":
        updated_dataframe = updated_dataframe[
            updated_dataframe["genre_list"].apply(lambda x: chosen_genre in x)
        ]

    if chosen_period != "All Periods":
        updated_dataframe = updated_dataframe[
            updated_dataframe["release_period"].astype(str) == chosen_period
        ]

    return updated_dataframe

#creates histogram plot for selected variable
def histogram_plot(dataframe, column_name, title, x_label):
    figure = px.histogram(
        dataframe,
        x=column_name,
        nbins=50
    )

    figure.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title=x_label,
        yaxis_title="Frequency"
    )

    return figure

#creates scatterplot and adds regression line
def scatterplot(dataframe, x_column, y_column, plot_title, x_label, y_label):
    figure = px.scatter(
        dataframe,
        x=x_column,
        y=y_column,
        hover_data=["title", "release_year"],
        opacity=0.35
    )

    if len(dataframe) > 1:
        x = dataframe[x_column]
        y = dataframe[y_column]
        coef = np.polyfit(x, y, 1)
        reg_line = np.poly1d(coef)
        sorted_x = np.sort(x)

        figure.add_scatter(
            x=sorted_x,
            y=reg_line(sorted_x),
            mode="lines",
            name="Regression line"
        )

    figure.update_layout(
        title=plot_title,
        title_x=0.5,
        xaxis_title=x_label,
        yaxis_title=y_label
    )

    return figure

#shows budget effect across different release periods
def barplot_budget_effect_period(dataframe):
    results = []

    periods = ["1990s", "2000s", "2010s", "2020-2025"]

    for period in periods:
        subset = dataframe[dataframe["release_period"].astype(str) == period]

        if len(subset) > 10:
            x = subset["log_budget"]
            y = subset["log_revenue"]
            slope = np.polyfit(x, y, 1)[0]

            results.append({
                "release_period": period,
                "budget_effect": slope
            })

    result_df = pd.DataFrame(results)

    figure = px.bar(
        result_df,
        x="release_period",
        y="budget_effect",
        title="Budget Effect across Release Periods",
        labels={
            "release_period": "Release Period",
            "budget_effect": "Budget Effect"
        }
    )

    figure.update_layout(
        title_x=0.5,
        xaxis_title="Release Period",
        yaxis_title="Budget Effect",
        showlegend=False
    )

    return figure

#shows budget effect across most common genres
def barplot_budget_effect_genre(dataframe):
    df = dataframe.copy().explode("genre_list")

    top_genres = df["genre_list"].value_counts().nlargest(6).index

    results = []

    for genre in top_genres:
        subset = df[df["genre_list"] == genre]

        if len(subset) > 10:
            x = subset["log_budget"]
            y = subset["log_revenue"]
            slope = np.polyfit(x, y, 1)[0]

            results.append({
                "genre": genre,
                "budget_effect": slope
            })

    result_df = pd.DataFrame(results)

    figure = px.bar(
        result_df,
        x="genre",
        y="budget_effect",
        title="Budget Effect across Genres",
        labels={
            "genre": "Genre",
            "budget_effect": "Budget Effect"
        }
    )

    figure.update_layout(
        title_x=0.5,
        xaxis_title="Genre",
        yaxis_title="Budget Effect",
        showlegend=False
    )

    return figure


#initial values
initial_genre = "All Genres"
initial_period = "All Periods"

filtered_initial = filter_data(livedata_q1, initial_genre, initial_period)

figure_hist_revenue_initial = histogram_plot(
    livedata_q1,
    column_name="revenue",
    title="Revenue Distribution",
    x_label="Revenue"
)

figure_hist_log_revenue_initial = histogram_plot(
    livedata_q1,
    column_name="log_revenue",
    title="Log Revenue Distribution",
    x_label="Log Revenue"
)

figure_scatter_initial = scatterplot(
    filtered_initial,
    x_column="log_budget",
    y_column="log_revenue",
    plot_title="Production Budget and Box Office Revenue",
    x_label="Log Production Budget",
    y_label="Log Box Office Revenue"
)

figure_bar_period_initial = barplot_budget_effect_period(livedata_q1)
figure_bar_genre_initial = barplot_budget_effect_genre(livedata_q1)

all_genres = sorted({genre for genres in livedata_q1["genre_list"] for genre in genres})

genre_options = [{"label": "All Genres", "value": "All Genres"}] + [
    {"label": genre, "value": genre}
    for genre in all_genres
]

period_options = [
    {"label": "All Periods", "value": "All Periods"},
    {"label": "1990s", "value": "1990s"},
    {"label": "2000s", "value": "2000s"},
    {"label": "2010s", "value": "2010s"},
    {"label": "2020-2025", "value": "2020-2025"}
]

#define layout
layout = html.Div([
    html.H1("How strongly does production budget predict box office revenue across different genres and release periods?"),
    html.H2("Context:"),
    html.P(
        "To answer this question, we collected movie data from the TMDB API for films released between 1990 and 2025. "
        "We focused on key variables such as production budget, box office revenue, genres, and release dates. "
        "After cleaning the dataset, we restricted the analysis to movies with valid budget and revenue values. "
        "We then applied a logarithmic transformation to reduce skewness in the revenue distribution. "
        "Finally, we analyzed the relationship between production budget and box office revenue overall, "
        "as well as across different genres and release periods."
    ),

    html.H2("Revenue distribution without log transformation", style={"textAlign": "left"}),
    dcc.Graph(
        id="hist-revenue",
        figure=figure_hist_revenue_initial
    ),

    html.H2("Revenue distribution with log transformation", style={"textAlign": "left"}),
    dcc.Graph(
        id="hist-log-revenue",
        figure=figure_hist_log_revenue_initial
    ),

    html.H2("Choose filters for the scatterplot", style={'textAlign': 'left'}),

    html.H3("Choose genre to analyse"),
    dcc.RadioItems(
        id="genre-selection",
        options=genre_options,
        value="All Genres",
        inline=True,
        style={'marginBottom': '20px', 'fontSize': '18px'}
    ),

    html.H3("Choose release period"),
    dcc.RadioItems(
        id="period-selection",
        options=period_options,
        value="All Periods",
        inline=True,
        style={'marginBottom': '20px', 'fontSize': '18px'}
    ),

    html.Button(
        "Update Values",
        id="start-button",
        n_clicks=0,
        style={"display": "block", "marginBottom": "20px", "marginTop": "20px", "padding": "10px", "fontSize": "16px"}
    ),

    dcc.Loading(
        id="loading-scatterplot",
        type="default",
        children=html.Div([
            dcc.Graph(
                id="main-plot",
                figure=figure_scatter_initial
            )
        ])
    ),

    html.H2("Budget Effect across Release Periods", style={"textAlign": "left"}),
    dcc.Graph(
        id="bar-period",
        figure=figure_bar_period_initial
    ),

    html.H2("Budget Effect across Genres", style={"textAlign": "left"}),
    dcc.Graph(
        id="bar-genre",
        figure=figure_bar_genre_initial
    ),

    html.H2("Take Away"),
    html.P(
        "Higher production budgets are positively associated with higher box office revenue. "
        "The relationship is consistent but not perfectly uniform, indicating that while budget is an important predictor of financial performance, "
        "its effect varies across genres and time periods and does not fully explain revenue outcomes."
    )
])

#refresh figures
@callback(
    Output("main-plot", "figure"),
    Input("start-button", "n_clicks"),
    State("genre-selection", "value"),
    State("period-selection", "value"),
    prevent_initial_call=True
)

def run_analysis(n_clicks, chosen_genre, chosen_period):
    if n_clicks == 0 or n_clicks is None:
        return dash.no_update

    updated_dataframe = filter_data(livedata_q1, chosen_genre, chosen_period)

    if len(updated_dataframe) == 0:
        return px.scatter(title="No data available for this selection")

    figure_scatter = scatterplot(
        updated_dataframe,
        x_column="log_budget",
        y_column="log_revenue",
        plot_title="Production Budget and Box Office Revenue",
        x_label="Log Production Budget",
        y_label="Log Box Office Revenue"
    )

    return figure_scatter
