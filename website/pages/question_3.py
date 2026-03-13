import dash
from dash import html, dcc, callback, Input, Output
import numpy as np
import pandas as pd
import io
import base64
import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import plotly.express as px

# register as new page
dash.register_page(__name__, name='Question 3: What are trends in the movie industry in terms of genre distribution and box office revenue from 2000 to 2025?')

data_2000 = pd.read_csv('pages/data_2000_2005.csv')
data_2025 = pd.read_csv('pages/data_2020_2025.csv')

#helper function

def explode_data(dataframe):
    """
    Explodes entries with mulitple genres so every genre has own entrie
    """
   
    dataframe_copy = dataframe.copy()  
    dataframe_copy['genres'] = dataframe_copy['genres'].astype(str).str.split(',')
    dataframe_exploded = dataframe_copy.explode('genres')
    dataframe_exploded['genres'] = dataframe_exploded['genres'].str.strip()
    
    return dataframe_exploded

def pie_chart(dataframe,columname="genres",topgenres=5,filter_zero=True,year=""):
    """
    Shows genre distributuion for x amount of genres and sums up the rest
    """
    #filter out movies with no box office 
    if filter_zero:
        if 'box_office_revenue' in dataframe.columns:
            dataframe = dataframe[dataframe['box_office_revenue']!= 0]

    # splitted multi genre movies into multiple entries with one genre
    dataframe_genres = explode_data(dataframe)

    allentries_count = dataframe_genres[columname].value_counts()
    #print(allentries_count)
    top_genres_plot = allentries_count.iloc[:topgenres]
    rest_genres_plot = allentries_count.iloc[topgenres:].sum()

    if rest_genres_plot > 0:
        rest_genres_series = pd.Series({'Rest': rest_genres_plot})
        plot_data = pd.concat([top_genres_plot,rest_genres_series])
    else:
        plot_data = top_genres_plot
    
    # variable title 
    if filter_zero:
        
        titel = f"Top {topgenres} Genres + Rest ({year})"
    else:
        filter_text = "all Movies Released"
        titel = f"Top {topgenres} Genres + Rest {filter_text} ({year})"

    #create plotly chart
    fig = px.pie(
        values=plot_data.values,          
        names=plot_data.index,            
        title=titel,                      
        color_discrete_sequence=px.colors.qualitative.Set3 
    )

    
    fig.update_traces(
        rotation=140, 
        textinfo='percent', 
        texttemplate='%{percent:.1%}' 
    )

    return fig

#generate pie charts
fig_2000 = pie_chart(dataframe=data_2000, topgenres=5, filter_zero=True, year="2000-2005")
fig_2025 = pie_chart(dataframe=data_2025, topgenres=5, filter_zero=True, year="2020-2025")



#define layout
layout = html.Div([
    html.H1("Pie chart with genre distribution"),
    
    # Der Slider
    html.Div([
        html.Label("Choose number of Top Genres from 1 to 12, other genres will be displayed as rest"),
        dcc.Slider(
            id='top-genres-slider',
            min=1,           
            max=12,          
            step=1,          
            value=10,         #default
            marks={i: str(i) for i in range(1, 16)} 
        )
    ], style={'padding': '20px', 'width': '80%', 'margin': 'auto'}),
    
    
    html.Div([
        dcc.Graph(id='pie-chart-2010')
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='pie-chart-2025')
    ], style={'width': '50%', 'display': 'inline-block'})
])


@callback(
    Output('pie-chart-2010', 'figure'),   #left
    Output('pie-chart-2025', 'figure'),   #right
    Input('top-genres-slider', 'value')   #change condistion in slider
)
def update_pie_charts(choosen_top_genres):
    """
    gets called when slider changes
    """
    fig_2000 = pie_chart( dataframe=data_2000, topgenres=choosen_top_genres, filter_zero=True, year="2000-2005")
    fig_2025 = pie_chart(dataframe=data_2025, topgenres=choosen_top_genres, filter_zero=True, year="2020-2025")
    
    
    return fig_2000, fig_2025


