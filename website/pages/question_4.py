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
dash.register_page(__name__,name ="question 4: ...")

csv =pd.read_csv('pages\q4\director_list.csv')

# helper function

def loading_data(csv):
    data = csv.copy()
    #print(directors.head())

    results = []

    for i in range(len(data)):

        df = pd.read_csv(f"pages\q4\director_{i}.csv")

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
        title='director popularity vs audience engagement with latest movie',
        labels={
            'hist_total_votes': 'total imdb votes',
            'new_votes' : 'new imdb votes'        
        },
        hover_name='director'
    )

    # Add regression line
    fig.add_traces(px.line(data, x='hist_total_votes', y='trendline').data)
    return fig

def load_and_clean_director_data(director_ids):

    data = {}

    for i in director_ids:
        df = pd.read_csv(f"pages\q4\director_{i}.csv")

        df = df.copy()
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df['avg_score'] = pd.to_numeric(df['avg_score'], errors='coerce')

        df = df.dropna(subset=['release_year','avg_score'])
        df = df.sort_values('release_year')

        data[i] = df

    return data

def plot_director_careers(director_ids):

    data= loading_data(csv)

    dfs = load_and_clean_director_data(director_ids)

    fig = go.Figure()

    for director_id, df in dfs.items():
        fig.add_trace(go.Scatter(
            x=df['release_year'],
            y=df['avg_score'],
            mode='lines+markers',
            name=data['director'][director_id]
        ))

    fig.update_layout(
        title='director career critical performance over time',
        xaxis_title = 'release year',
        yaxis_title  = 'average score'
    )    
    
    return fig




    
def load_budget_revenue_data(director_ids):
    data = loading_data(csv)

    dfs = []

    for i in director_ids:
        df = pd.read_csv(f"pages\q4\director_{i}.csv")

        df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

        df = df.dropna(subset=['budget', 'revenue'])

        df['roi'] = df['revenue']/df['budget']
        df['director_id'] = i
        df['name'] = data['director'][i]

        dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()
    
    return pd.concat(dfs, ignore_index=True)

def plot_budget_vs_revenue(director_ids):
    df = load_budget_revenue_data(director_ids)

    if df.empty:
        return {}
    fig = px.scatter(
        df,
        x='budget',
        y='revenue',
        color='roi',
        symbol='name',
        hover_name='name',
        log_x=True,
        log_y=True,
        title='budget vs revenue (roi colored)',
        labels={
            'budget': 'budget(log scale)',
            'revenue' : 'revenue (log scale)',
            'roi' : 'ROI'
        },
        color_continuous_scale='Viridis'
    )
    return fig


popularity = popularity_scatter(csv)
avg_score = avg_score_scatter(csv)
financial = financial_success_scatter(csv)

layout = html.Div([

    html.H1("How does the historical success over the last 30-40 years of the 10 most popular active directors influence the financial and critical success of their new movie releases?"),
    html.H2("Context"),
    html.P(""),

    html.H1("Historical data vs newest movie data per director"),

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
        html.H2('plot', style={'marginTop': '50px'}),
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
        html.H2('plot', style={'marginTop': '50px'}),
        dcc.Dropdown(
            id='director2-dropdown',
            options=[
                {'label': csv['name'][i], 'value': i}
                for i in range(len(csv))
            ],
            value=[0],      #default selection
            multi=True      # allows multiple selection
        ),
        dcc.Graph(id='budget-revenue-plot')

    ]),


    html.P("")
])


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
def update_career_plot(selected_directors):
    if not selected_directors:
        return {}
    return plot_budget_vs_revenue(selected_directors)