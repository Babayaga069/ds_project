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
dash.register_page(__name__,name ="Question: 4",order=4)

csv =pd.read_csv('pages/q4/director_list.csv')

# helper function loading and preprocessing data

def loading_data(csv):
    data = csv.copy()

    results = []

    for i in range(len(data)):

        df = pd.read_csv(f"pages/q4/director_{i}.csv")

        # sort movies by year
        df = df.sort_values('release_year')

        # latest movie
        latest = df.iloc[-1]

        # historical movies
        historical = df.iloc[:-1]

        hist_avg_score = historical["avg_score"].mean()
        hist_avg_roi  = (historical['revenue'] / historical['budget']).mean()
        hist_avg_revenue = historical['revenue'].mean()
        hist_votes = historical['imdb_vote_count'].sum()

        new_score = latest['avg_score']
        new_roi = latest['revenue']/latest['budget']
        new_revenue = latest['revenue']
        new_votes = latest['imdb_vote_count']

        results.append({
            'director' : data['name'][i],
            'hist_avg_score' : hist_avg_score,
            'hist_avg_roi' : hist_avg_roi,
            'hist_avg_revenue' : hist_avg_revenue,
            'hist_total_votes' : hist_votes,
            'new_score' : new_score,
            'new_roi' : new_roi,
            'new_revenue' : new_revenue,
            'new_votes' : new_votes 
        })

    analysis_df = pd.DataFrame(results)

    #corr = analysis_df.corr(numeric_only=True)

    return analysis_df

# Plot newest movie's scores over historical average scores per directors in scatterplot with regression line
def avg_score_scatter(data):
    data = loading_data(data)
    x = data['hist_avg_score']
    y= data['new_score']

    # Fit linear regression
    m, b = np.polyfit(x,y,1)
    trendline = m*x+b

    # Add trendline as a seperate column for Plotly
    data['trendline'] = trendline

    fig = px.scatter(
        data,
        x='hist_avg_score',
        y ='new_score',
        color='director',
        title='Historical Critical Success vs Newest Movie Score',
        labels={
            'hist_avg_score': 'Historical Average Score per Director',
            'new_score' : 'Newest Movie Score'        
        },
        hover_name='director'
    )

    # Add regression line
    fig.add_traces(px.line(data, x='hist_avg_score', y='trendline').data)
    return fig

# Plot newest movie's ROI over historical average ROI per directors in scatterplot with regression line
def financial_success_scatter(csv):
    data = loading_data(csv)
    x = data['hist_avg_roi']
    y= data['new_roi']

    # Fit linear regression
    m, b = np.polyfit(x,y,1)
    trendline = m*x+b

    # Add trendline as a seperate column
    data['trendline'] = trendline

    fig = px.scatter(
        data,
        x='hist_avg_roi',
        y='new_roi',
        color='director',
        title='Historical Financial Success vs Newest Movie Return Of Invest (ROI)',
        labels={
            'hist_avg_roi': 'Historical Average ROI',
            'new_roi' : 'New Movie ROI'
        },
        hover_name = 'director'
    )

    # Add regression line
    fig.add_traces(px.line(data, x='hist_avg_roi', y='trendline').data)
    return fig

# Plot newest movie's IMDb vote count over historical total IMDb vote count per directors in scatterplot with regression line
def popularity_scatter(csv):
    data = loading_data(csv)
    x = data['hist_total_votes']
    y = data['new_votes']

    # Fit linear regression
    m, b = np.polyfit(x,y,1)
    trendline = m*x+b
    
    # Add trendline as a seperate column
    data['trendline'] = trendline

    fig = px.scatter(
        data,
        x='hist_total_votes',
        y ='new_votes',
        color='director',
        title='Director Popularity vs Audience Engagement with latest Movie',
        labels={
            'hist_total_votes': 'Total IMDb Votes across all Movies per Director',
            'new_votes' : 'Newest Movie IMDb Votes'        
        },
        hover_name='director'
    )

    # Add regression line
    fig.add_traces(px.line(data, x='hist_total_votes', y='trendline').data)
    return fig

# helper function loading and preprocessing data for director career timeline
def load_and_clean_director_data(director_ids):

    data = {}

    for i in director_ids:
        df = pd.read_csv(f"pages/q4/director_{i}.csv")

        df = df.copy()
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df['avg_score'] = pd.to_numeric(df['avg_score'], errors='coerce')

        df = df.dropna(subset=['release_year','avg_score'])
        df = df.sort_values('release_year')

        data[i] = df

    return data

# Plotting director's movie scores across release years for chosen directors with graph
def plot_director_careers(director_ids):

    data= loading_data(csv)

    dfs = load_and_clean_director_data(director_ids)

    fig = go.Figure()

    for director_id, df in dfs.items():
        fig.add_trace(go.Scatter(
            x=df['release_year'],
            y=df['avg_score'],
            mode='lines+markers',
            name=data['director'][director_id],
            text=df['title'],  # assuming titles exist
            hovertemplate=
                '<b>%{text}</b><br>' +   # movie title
                'Director: ' + data['director'][director_id] + '<br>' +
                'Year: %{x}<br>' +
                'Score: %{y}<br>' +
                '<extra></extra>'
        ))

    fig.update_layout(
        title='Director Career Critical Performance over Time',
        xaxis_title = 'Release Year',
        yaxis_title  = 'Average Score'
    )    
    
    return fig


# helper function loading and preprocessing each movie's data for revenue over budget for chosen director
def load_budget_revenue_data(director_id):
    data = loading_data(csv)

    df = pd.read_csv(f"pages/q4/director_{director_id}.csv")

    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

    df = df.dropna(subset=['budget', 'revenue'])

    df['roi'] = df['revenue']/df['budget']
    df['director_id'] = director_id
    df['name'] = data['director'][director_id]
    df['title'] = df['title']

    return df

# Plotting movie's revenue over budget for all movies of chosen director in heat scatter plot
def plot_budget_vs_revenue(director_id):
    
    df = load_budget_revenue_data(director_id)

    if df.empty:
        return {}
    fig = px.scatter(
        df,
        x='budget',
        y='revenue',
        color='roi',
        hover_name='title',
        log_x=True,
        log_y=True,
        title='Budget vs Revenue (ROI colored)',
        labels={
            'budget': 'Budget (log scale)',
            'revenue' : 'Revenue (log scale)',
            'roi' : 'ROI'
        },
        color_continuous_scale='RdYlGn'
    )
    return fig

# initial values and plots

popularity = popularity_scatter(csv)
avg_score = avg_score_scatter(csv)
financial = financial_success_scatter(csv)

# LAYOUT
layout = html.Div([

    html.H1("How does the historical success over the last 30-40 years of the 10 most popular active directors influence the financial and critical success of their new movie releases?"),
    html.H2("Context"),
    html.P("The 10 most popular directors have built a strong reputation over the last 40 years, through critically acclaimed and financially successfull movies. \
    In this analysis we compare the past performances of directors by looking at all their movies and compare it with their latest movie release. \
    Using the financial success, critical success, popurality "),

    html.H2("Historical Data vs Newest Movie Data per Director"),
    html.P('The following graphs all show the performance of all previous movies and their performances of a director, compared to the newest movie. \
    It compares the Return of Invest for financial success, the rating scores achieved for the critical success and the amount of IMDb votes for general popularity of each director.'),


    html.Div([
        dcc.Graph(figure=financial)
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(figure=avg_score)
    ], style={'width': '50%', 'display' :'inline-block'}),

    html.Div([
        dcc.Graph(figure=popularity)
    ], style={'width': '50%', 'display': 'iline-block'}),


    html.Div([
        html.H2('Director Performance Timeline', style={'marginTop': '50px'}),
        dcc.Dropdown(
            id='director1-dropdown',
            options=[
                {'label': csv['name'][i], 'value': i}
                for i in range(len(csv))
            ],
            value=[0],      #default selection
            multi=True      # allows multiple selection
        ),
        dcc.Graph(id='career-plot')

    ]),

    html.Div([
        html.H2('Return of Invest Analysis per Director', style={'marginTop': '50px'}),
        dcc.Dropdown(
            id='director2-dropdown',
            options=[
                {'label': csv['name'][i], 'value': i}
                for i in range(len(csv))
            ],
            value=0,      #default selection
            multi=False      # allows multiple selection
        ),
        dcc.Graph(id='budget-revenue-plot')

    ]),

    html.H1('Take Away'),
    html.P("Generally speaking it's visible that there is a modest relationship between historical success and new release performance, although it's stranger for critical scores and audience engangement than for financial returns \
    With the critical success the relationship between historical performance and newest movie performance is clear, that directors with consistently high historical average scores tend to maintain strong critical scores. \
    It's similar wit the audience engagement as well, especially with historically popular directors like Steven Spielberg or Christopher Nolan. The relationship is less seen with financial success. \
    It's safe to say that historical success provides some predictive signal, particularly for critical reception and audience engagement, but is a weak predictor of financial outcomes, where external factors (marketing, genre, timing) introduce substantial variability.")
])

# updating figures
@callback(
    Output('career-plot', 'figure'),
    Input('director1-dropdown', 'value')
)
def update_career_plot(selected_directors):
    if not selected_directors:
        return {}
    return plot_director_careers(selected_directors)

@callback(
    Output('budget-revenue-plot', 'figure'),
    Input('director2-dropdown', 'value')
)
def update_career_plot(selected_director):
    return plot_budget_vs_revenue(selected_director)