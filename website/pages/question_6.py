import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(
    __name__,
    name="Question: 5",order=5
)

# Data
df = pd.read_csv("pages/Q6.csv")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year

sequels = df[df["part"] > 0].copy()
originals = df[df["part"] == 0].copy()

def performance_boxplot(originals, sequels):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=["Revenue ($)", "Return on Investment", "Audience Rating"]
    )

    # Revenue
    fig.add_trace(go.Box(y=originals["revenue"], name="Original", boxmean=True), row=1, col=1)
    fig.add_trace(go.Box(y=sequels["revenue"], name="Sequel", boxmean=True), row=1, col=1)

    # ROI
    fig.add_trace(go.Box(y=originals["roi"], name="Original", boxmean=True), row=1, col=2)
    fig.add_trace(go.Box(y=sequels["roi"], name="Sequel", boxmean=True), row=1, col=2)

    # Rating
    fig.add_trace(go.Box(y=originals["rating"], name="Original", boxmean=True), row=1, col=3)
    fig.add_trace(go.Box(y=sequels["rating"], name="Sequel", boxmean=True), row=1, col=3)

    fig.update_layout(
        title="Original vs Sequel: Financial and Critical Performance",
        showlegend=False,
        height=500
    )

    return fig


def performance_by_part(sequels, max_part):
    filtered = sequels[sequels["part"] <= max_part]

    by_part = filtered.groupby("part").agg(
        revenue_diff=("revenue_diff", "mean"),
        rating_diff=("rating_diff", "mean")
    ).reset_index()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=by_part["part"],
        y=by_part["revenue_diff"],
        name="Revenue difference"
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=by_part["part"],
        y=by_part["rating_diff"],
        mode="lines+markers",
        name="Rating difference"
    ), secondary_y=True)

    fig.update_yaxes(title_text="Revenue difference", secondary_y=False)
    fig.update_yaxes(title_text="Rating difference", secondary_y=True)
    fig.update_layout(
        title="Performance Change Compared to Original Film",
        xaxis_title="Sequel number (1 = first sequel)",
        legend_title=""
    )

    return fig


# Figures
fig_box = performance_boxplot(originals, sequels)

# Layout
layout = html.Div([
    html.H1("How does the financial and critical success of movie sequels between 2010 and 2024 compare to their original films across franchises?"),
    html.H2("Context"),
    html.P(
        "Many successful movies become franchises and produce several sequels. "
        "This analysis compares financial success (box office revenue and ROI) "
        "and critical success (ratings) between original movies and their sequels."
    ),

    html.H2("Original vs Sequel Performance"),
    dcc.Graph(figure=fig_box, style={"width": "90%"}),

    html.H2("Performance depending on sequel number"),
    html.P(
        "A value above zero means that the sequel performed better than the original. "
        "Negative values indicate worse performance."
    ),

    html.Label("Choose the maximum sequel number to include"),
    dcc.Slider(
        id="sequel-slider",
        min=1,
        max=int(sequels["part"].max()),
        step=1,
        value=3,
        marks={i: str(i) for i in range(1, int(sequels["part"].max()) + 1)},
        tooltip={"placement": "bottom"}
    ),

    dcc.Graph(id="sequel-performance-graph", style={"width": "90%"}),

    html.H2("Take Away"),
    html.P(
        "On average, sequels underperform their originals financially and critically. "
        "Some sequels achieve higher revenue than the original, but many earn less "
        "and receive slightly worse ratings. Sequel success depends on the franchise."
    )
])


@callback(
    Output("sequel-performance-graph", "figure"),
    Input("sequel-slider", "value")
)
def update_graph(max_part):
    return performance_by_part(sequels, max_part)