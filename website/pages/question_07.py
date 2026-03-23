import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import ast
import plotly.express as px

# register as new page
dash.register_page(__name__, name='Question: 6',order=6)

livedata_q2 = pd.read_csv('pages/q7/oscars_movies_merged.csv')

# parse stored genre strings
livedata_q2["genre_list"] = livedata_q2["genre_list"].apply(
    lambda x: ast.literal_eval(x) if pd.notna(x) else []
)
# create budget groups
livedata_q2["budget_group"] = pd.qcut(livedata_q2["budget"], 5)

# explode genre list for genre based analysis
data_genres_cached = livedata_q2.explode("genre_list").copy()
data_genres_cached = data_genres_cached.rename(columns={"genre_list": "genre"})

#creates binary column for chosen nomination threshold
def nomination_column(dataframe, threshold):
    updated_dataframe = dataframe.copy()
    updated_dataframe["nomination_binary"] = (updated_dataframe["oscar_nominations"] >= threshold).astype(int)
    return updated_dataframe

#shows oscar nomination probability by genre
def genre_barchart(dataframe, threshold):
    updated_dataframe = nomination_column(dataframe, threshold)

    genre_stats = (
        updated_dataframe.groupby("genre")
        .agg(
            nomination_rate=("nomination_binary", "mean"),
            n_movies=("nomination_binary", "count")
        )
    )
    #filter out genres with too few movies
    genre_stats = genre_stats[genre_stats["n_movies"] >= 100]
    genre_stats = genre_stats.sort_values("nomination_rate", ascending=True).reset_index()

    figure = px.bar(
        genre_stats,
        x="nomination_rate",
        y="genre",
        orientation="h",
        title=f"Oscar nomination probability by genre (at least {threshold} nomination{'s' if threshold > 1 else ''})",
        labels={"nomination_rate": "Oscar nomination rate", "genre": "Genre"}
    )

    figure.update_layout(
        title_x=0.5,
        yaxis_title="Genre",
        xaxis_title="Oscar nomination rate"
    )

    return figure

#shows oscar nomination probability by budget group
def budget_barchart(dataframe, threshold):
    updated_dataframe = nomination_column(dataframe, threshold)

    budget_stats = (
        updated_dataframe.groupby("budget_group")
        .agg(
            nomination_rate=("nomination_binary", "mean"),
            n_movies=("nomination_binary", "count")
        )
        .reset_index()
    )
     # create labels for budget groups
    labels = [
        f"${int(interval.left/1e6)}M–${int(interval.right/1e6)}M"
        for interval in budget_stats["budget_group"]
    ]

    budget_stats["budget_label"] = labels

    figure = px.bar(
        budget_stats,
        x="budget_label",
        y="nomination_rate",
        title=f"Oscar nomination probability by budget group (at least {threshold} nomination{'s' if threshold > 1 else ''})",
        labels={"budget_label": "Budget group (Million USD)", "nomination_rate": "Oscar nomination rate"}
    )

    figure.update_layout(
        title_x=0.5,
        xaxis_title="Budget group (Million USD)",
        yaxis_title="Oscar nomination rate"
    )

    return figure

#shows oscar nomination rate by genre and budget group
def heatmap_plot(dataframe):
    valid_genres = (
        dataframe.groupby("genre")
        .agg(n_movies=("oscar_nominated", "count"))
    )
    valid_genres = valid_genres[valid_genres["n_movies"] >= 100].index

    filtered_dataframe = dataframe[dataframe["genre"].isin(valid_genres)].copy()

    genre_budget_stats = (
        filtered_dataframe.groupby(["genre", "budget_group"])
        .agg(
            nomination_rate=("oscar_nominated", "mean"),
            n_movies=("oscar_nominated", "count")
        )
        .reset_index()
    )
    # filter out genre budget groups with too few movies
    genre_budget_stats = genre_budget_stats[genre_budget_stats["n_movies"] >= 5]

    genre_budget_matrix = genre_budget_stats.pivot(
        index="genre",
        columns="budget_group",
        values="nomination_rate"
    )
     # create labels for heatmap columns
    heatmap_columns = [
        f"${int(interval.left/1e6)}M–${int(interval.right/1e6)}M"
        for interval in genre_budget_matrix.columns
    ]

    genre_budget_matrix.columns = heatmap_columns

    figure = px.imshow(
        genre_budget_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="viridis"
    )

    figure.update_layout(
        title="Oscar nomination rate by genre and budget group",
        title_x=0.5,
        xaxis_title="Budget group (Million USD)",
        yaxis_title="Genre",
        coloraxis_colorbar_title="Oscar nomination rate"
    )

    return figure

# initial values
initial_threshold = 1

figure_genre_initial = genre_barchart(data_genres_cached, threshold=initial_threshold)
figure_budget_initial = budget_barchart(livedata_q2, threshold=initial_threshold)
figure_heatmap_initial = heatmap_plot(data_genres_cached)

# define layout
layout = html.Div([
    html.H1("How does movie genre, along with production budget, influence the likelihood of receiving an Academy Award nomination?"),
    html.H2("Context:"),
    html.P(
        "To answer this question, we combined movie data with Oscar nomination information and focused on film genre, production budget, "
        "and nomination counts. We assigned each movie to all listed genres, grouped budgets into five categories, and then examined how "
        "nomination probabilities change across genres and budget levels. Finally, the page allows the user to choose a minimum nomination threshold "
        "in order to compare how the results change for films with more Oscar nominations."
    ),
    html.H2("Oscar nomination probability across genres and budget groups", style={"textAlign": "left"}),

    html.Label("Choose minimum number of Oscar nominations"),
    dcc.Slider(
        id="threshold-slider",
        min=1,
        max=14,
        step=1,
        value=1,
        marks={i: str(i) for i in range(1, 15)},
    ),

    dcc.Loading(
        id="loading-bar-charts",
        type="default",
        children=html.Div([
            dcc.Graph(
                id="genre-barplot",
                figure=figure_genre_initial,
                style={"display": "inline-block", "width": "50%"}
            ),
            dcc.Graph(
                id="budget-barplot",
                figure=figure_budget_initial,
                style={"display": "inline-block", "width": "50%"}
            ),
        ])
    ),

    html.H2("Oscar nomination rate by genre and budget group", style={"textAlign": "left"}),

    dcc.Graph(
        id="heatmap-plot",
        figure=figure_heatmap_initial
    ),
    html.H2("Take Away"),
    html.P(
        "Oscar nomination rates differ substantially across film genres and budget groups. In general, films with higher production budgets are more likely to receive an Oscar nomination, but this relationship varies by genre. Genres such as history, drama, and animation tend to show higher nomination probabilities, whereas horror, thriller, and crime films are nominated less frequently overall. These results suggest that both genre and budget are associated with Oscar nomination likelihood."
    )
])

#refresh figure
@callback(
    Output("genre-barplot", "figure"),
    Output("budget-barplot", "figure"),
    Input("threshold-slider", "value")
)
def run_analysis(chosen_threshold):
    figure_genre = genre_barchart(data_genres_cached, threshold=chosen_threshold)
    figure_budget = budget_barchart(livedata_q2, threshold=chosen_threshold)

    return figure_genre, figure_budget