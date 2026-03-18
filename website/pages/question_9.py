import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

dash.register_page(__name__, name='Question:9')

# Load data
df = pd.read_csv("pages/q9/Q9.csv")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year
df_clean = df.dropna(subset=["avg_trend_before", "avg_trend_after"]).copy()

# static
top10_pre = df_clean.sort_values("avg_trend_before", ascending=False).head(10)
fig_top10_pre = px.bar(
    top10_pre,
    x="title",
    y="avg_trend_before",
    color="revenue",
    title="Top 10 Movies by Pre-Release Search Interest",
    labels={"avg_trend_before": "Avg. Search Interest", "title": "Movie Title", "revenue": "Revenue ($)"}
)
fig_top10_pre.update_layout(xaxis_tickangle=-45)

# Dynamic 
def scatter_figure(y_metric):
    fig = px.scatter(
        df_clean,
        x="avg_trend_before",
        y=y_metric,
        hover_data=["title", "release_year", "revenue", "roi", "vote_average"],
        title=f"Pre-Release Search Interest vs. {y_metric.replace('_',' ').title()}"
    )
    fig.update_layout(xaxis_title="Avg. Search Interest (6 months before release)")
    return fig

layout = html.Div([
    html.H2("Pre-Release Search Interest Analysis"),

    html.Label("Select Metric for Y-axis"),
    dcc.Dropdown(
        id="y-metric-dropdown",
        options=[
            {"label": "Revenue", "value": "revenue"},
            {"label": "ROI", "value": "roi"},
            {"label": "Average Rating", "value": "vote_average"}
        ],
        value="revenue",
        clearable=False,
        style={"width": "300px"}
    ),

    dcc.Graph(id="dynamic-scatter", figure=scatter_figure("revenue")),

    html.H3("Top 10 Movies by Pre-Release Interest"),
    dcc.Graph(figure=fig_top10_pre)
])

@callback(
    Output("dynamic-scatter", "figure"),
    Input("y-metric-dropdown", "value")
)
def update_scatter(y_metric):
    return scatter_figure(y_metric)