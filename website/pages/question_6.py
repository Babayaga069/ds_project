import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

dash.register_page(
    __name__,
    name="Question 6: Sequel vs Original Performance"
)

# Data
df = pd.read_csv("pages/sequel_analysis.csv")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year

sequels = df[df["part"] > 0].copy()
originals = df[df["part"] == 0].copy()

# helper
def performance_boxplot(originals, sequels):
    metrics = {"revenue": "Revenue ($)", "roi": "Return on Investment", "rating": "Audience Rating"}
    fig = go.Figure()
    for col, label in metrics.items():
        fig.add_trace(go.Box(y=originals[col], name=f"Original – {label}", boxmean=True))
        fig.add_trace(go.Box(y=sequels[col], name=f"Sequel – {label}", boxmean=True))
    fig.update_layout(title="Original vs Sequel: Financial and Critical Performance", yaxis_title="Value", showlegend=False)
    return fig

def performance_by_part(sequels, max_part):
    filtered = sequels[sequels["part"] <= max_part]
    by_part = filtered.groupby("part").agg(revenue_diff=("revenue_diff", "mean"), rating_diff=("rating_diff", "mean")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=by_part["part"], y=by_part["revenue_diff"], name="Revenue difference"))
    fig.add_trace(go.Scatter(x=by_part["part"], y=by_part["rating_diff"], mode="lines+markers", name="Rating difference"))
    fig.add_hline(y=0)
    fig.update_layout(title="Performance Change Compared to Original Film",
                      xaxis_title="Sequel number (1 = first sequel)",
                      yaxis_title="Difference vs original",
                      legend_title="")
    return fig

# figure
fig_box = performance_boxplot(originals, sequels)

# layout
layout = html.Div([
    html.H2("Context"),
    html.P("Many successful movies become franchises and produce several sequels. "
           "This analysis compares financial success (box office revenue and ROI) and critical success (ratings) "
           "between original movies and their sequels."),

    html.H2("Original vs Sequel Performance"),
    dcc.Graph(figure=fig_box, style={"width": "80%"}),

    html.H2("Performance depending on sequel number"),
    html.P("A value above zero means that the sequel performed better than the original. Negative values indicate worse performance."),
    
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

    dcc.Graph(id="sequel-performance-graph", style={"width": "80%"}),

    html.H2("Take Away"),
    html.P("On average, sequels underperform their originals financially and critically. "
           "Some sequels achieve higher revenue than the original, but many earn less and receive slightly worse ratings. "
           "Sequel success strongly depends on the specific franchise.")
])

# Callback
@callback(
    Output("sequel-performance-graph", "figure"),
    Input("sequel-slider", "value")
)
def update_graph(max_part):
    return performance_by_part(sequels, max_part)