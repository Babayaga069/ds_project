import dash
from dash import html, dcc, callback, Input, Output
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# register as new page
dash.register_page(__name__, name='Question: 3',order=3)

data_2000 = pd.read_csv('pages/q3/data_2000_2005.csv')
data_2025 = pd.read_csv('pages/q3/data_2020_2025.csv')

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
    genre_color={
    'Drama': '#8dd3c7',
    'Comedy': '#ffffb3',
    'Romance': '#bebada',
    'Thriller': '#fb8072',
    'Action': '#80b1d3',
    'Crime': '#fdb462',
    'Adventure': '#b3de69',
    'Family': '#fccde5',
    'Horror': '#d9d9d9',
    'Mystery': '#bc80bd',
    'Fantasy': '#ccebc5',
    'Rest': '#e0e0e0',           
    'Science Fiction': '#a6cee3', 
    'Animation': '#ff9f9b',      
    'History': '#d4a6c8',        
    'Music': '#8c96c6',           
    'Documentary': '#ffd92f'   
       }   
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
        color= plot_data.index,
        color_discrete_map=genre_color
    )

    
    fig.update_traces(
        rotation=140, 
        textinfo='percent', 
        texttemplate='%{percent:.1%}' 
    )

    return fig


def plot_growth(dataframe_old, dataframe_new, column='genres', year_old="2000-2005", year_new="2020-2025", filter_zero=True):
    """
    Shows relativ Growth of genres from one time frame to another
    """
    if filter_zero:
        if 'box_office_revenue' in dataframe_old.columns:
            dataframe_old = dataframe_old[dataframe_old['box_office_revenue'] != 0]
        if 'box_office_revenue' in dataframe_new.columns:
            dataframe_new = dataframe_new[dataframe_new['box_office_revenue'] != 0]

    # split genre list to to single genre entries
    dataframe_old = explode_data(dataframe_old)
    dataframe_new = explode_data(dataframe_new)

    # Calculate relativ split of genre
    count_old = dataframe_old[column].value_counts(normalize=True)
    count_new = dataframe_new[column].value_counts(normalize=True)

    # Merge
    dataframe_compare = pd.DataFrame({f'Year_{year_old}': count_old, f'Year_{year_new}': count_new}).fillna(0)

    # filter out unimporantant genre
    dataframe_compare = dataframe_compare[(dataframe_compare[f'Year_{year_old}'] + dataframe_compare[f'Year_{year_new}']) >= 0.01]

    dataframe_compare['Growth (%)'] = np.where(dataframe_compare[f'Year_{year_old}'] == 0, 100.0, ((dataframe_compare[f'Year_{year_new}'] - dataframe_compare[f'Year_{year_old}']) / dataframe_compare[f'Year_{year_old}']) * 100)
    dataframe_compare = dataframe_compare.sort_values(by = 'Growth (%)')

    
    colorbar = ['#d62728' if x < 0 else '#2ca02c' for x in dataframe_compare['Growth (%)']]
    
   
    fig = px.bar(
        dataframe_compare,
        x='Growth (%)',
        y=dataframe_compare.index,
        orientation='h'
    )
    fig.update_traces(marker_color=colorbar)
    
    
    fig.add_vline(x=0, line_color='black', line_width=1.5)

    
    min_val = dataframe_compare['Growth (%)'].min()
    max_val = dataframe_compare['Growth (%)'].max()
    fig.update_xaxes(range=[min_val - 15, max_val + 15])

    
    for index, row in dataframe_compare.iterrows():
        
        bar_width = row['Growth (%)'] 
        genre_name = index 
        
        
        x_position = bar_width + (2 if bar_width > 0 else -2)
        direction = 'left' if bar_width > 0 else 'right'
        
       
        fig.add_annotation(
            x=x_position,
            y=genre_name,
            text=f"{bar_width:+.1f}%",
            showarrow=False,                 
            font=dict(color='black', size=10),
            xanchor=direction,               
            yanchor='middle'                 
        )


    
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    
    return fig

def plot_toal_boxoffice(dataframe_old, dataframe_new, year_old="2000-2005", year_new="2020-2025", box_office='box_office_revenue', inflation_factor=1.6):
    """
    Compares total box_office revenue of two timeframes
    """
    
    total_old = (dataframe_old[box_office].sum() * inflation_factor) / 1000000000
    total_new = dataframe_new[box_office].sum() / 1000000000

    
    if inflation_factor != 1.0:
        titel_text = f'Combined revenue (Inflation corrected for {year_old})'
    else:
        titel_text = 'Combined revenue'
        
    y_label_text = 'Revenue in billion USD'

    
    fig = px.bar(
        x=[f'Year {year_old}', f'Year {year_new}'],  
        y=[total_old, total_new],                    
        title=titel_text,
        labels={'x': '', 'y': y_label_text}         
    )

    
    fig.update_traces(marker_color=['#1f77b4', '#ff7f0e'])

    
    fig.update_layout(width=700, height=600)

    
    return fig

def plot_genre_comp(dataframe_old, dataframe_new, genre_list, year_old="2000-2005", year_new="2020-2025", column='genres', box_office='box_office_revenue', inflation_factor=1.6):
    """
    Compares The financial success of same genres in different time frames
    """
    
    # split multi genre movies
    dataframe_old = explode_data(dataframe_old)
    dataframe_new = explode_data(dataframe_new)
    
    # filter moviegenres out
    dataframe_old_filterd = dataframe_old[dataframe_old[column].isin(genre_list)]
    dataframe_new_filterd = dataframe_new[dataframe_new[column].isin(genre_list)]
    
    # calculate genre revenue
    box_old = (dataframe_old_filterd.groupby(column)[box_office].sum() * inflation_factor / 1000000)
    box_new = (dataframe_new_filterd.groupby(column)[box_office].sum() / 1000000)
    
    dataframe_revenue = pd.DataFrame({f'{year_old}': box_old, f'{year_new}': box_new}).fillna(0)
    
   
    fig = px.bar(
        dataframe_revenue,
        barmode='group',  
        color_discrete_sequence=['#1f77b4', '#ff7f0e'], 
        title='Financial Comparrision between genres'
    )

    
    fig.update_layout(
        xaxis_title='',                             
        yaxis_title='Revenue in Million USD',       
        xaxis_tickangle=0,                         
        legend_title_text=''                       
    )

    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', griddash='dash')


    return fig


#
genres = ['Fantasy']
#generate pie charts
fig_pie_2000 = pie_chart(data_2000, topgenres=5, filter_zero=True, year="2000-2005")
fig_pie_2025 = pie_chart(data_2025, topgenres=5, filter_zero=True, year="2020-2025")

fig_growth = plot_growth(data_2000,data_2025)
fig_total = plot_toal_boxoffice(data_2000,data_2025)
fig_compare = plot_genre_comp(data_2000,data_2025,genre_list=genres)



#define layout
layout = html.Div([

    html.H1("What are trends in the movie industry in terms of genre distribution and box office revenue from 2000 to 2025?"),
    html.H2("Context:"),
    html.P("To answer this question we only considered data from the TMDB API for the times 2000-2005 and 2020-2025. " \
    "To keep data relevant we filtered out all movies with $0 global box office revenue. " \
    " For the financial comparison, we applied an inflation factor of 1.6 to the data from 2000-2005.    We calculated this factor using 2003 and 2023 as our " \
    "representative base years to keep it simple. All financial data is presented in US Dollars (USD)."),
    html.H1("Pie chart with genre distribution"),
    
    # slider
    html.Div([
        html.Label("Choose number of Top Genres from 1 to 15, other genres will be displayed as rest"),
        dcc.Slider(
            id='top-genres-slider',
            min=1,           
            max=15,          
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
    ], style={'width': '50%', 'display': 'inline-block'}),

    # Genre  Growth Figure

    html.H2("Relativ Genre Growth"),

    html.Div([
        dcc.Graph(figure=fig_growth)  
    ], style={'width': '50%', 'marginTop': '50px'}),

    html.Div([
        html.H2("Box Office Analyse", style={'marginTop': '50px'}),
        
        dcc.Dropdown(
            id='box-office-dropdown',
            options=[
                {'label': 'Compare total box office', 'value': 'total'},
                {'label': 'Compare genre box office', 'value': 'genres'}
            ],
            value='total',
            style={'width': '20%', 'marginBottom': '20px'}
        ),

        # Double drop down menu for selection of compare 
        html.Div(id='genre-selection-container', children=[
            html.Label("Which Genre you want to compare"),
            dcc.Dropdown(
                id='genre-multi-select',
                
                options=[
                    {'label': 'Action', 'value': 'Action'},
                    {'label': 'Comedy', 'value': 'Comedy'},
                    {'label': 'Drama', 'value': 'Drama'},
                    {'label': 'Fantasy', 'value': 'Fantasy'},
                    {'label': 'Horror', 'value': 'Horror'},
                    {'label': 'Sci-Fi', 'value': 'Science Fiction'},
                    {'label': 'Adventure', 'value': 'Adventure'},
                    {'label': 'Romance', 'value': 'Romance'}],
                value=['Action'], #Default
                multi=True, 
                style={'width': '20%', 'marginBottom': '20px'}
            )
        ], style={'display': 'none'}), 
        
        dcc.Graph(
            id='box-office-graph',
            style={'height': '700px', 'width': '200%'})
    ], style={'width': '150%', 'padding': '20px'}),

    html.H2("Take Away:"),
    html.P("The movie industry saw a steep revenue drop, reflecting shifts in the audience, both in how we watch movies and what genres we choose. Even though the top genres seem stable, their market share shrank, making room for a more diverse genre distribution."),

        

    
])


@callback(
    Output('pie-chart-2010', 'figure'),   #left
    Output('pie-chart-2025', 'figure'),   #right
    Input('top-genres-slider', 'value')   #change condtion in slider

)
def update_pie_charts(choosen_top_genres):
    """
    gets called when slider changes
    """
    fig_pie_2000 = pie_chart( dataframe=data_2000, topgenres=choosen_top_genres, filter_zero=True, year="2000-2005")
    fig_pie_2025 = pie_chart(dataframe=data_2025, topgenres=choosen_top_genres, filter_zero=True, year="2020-2025")
    
    
    return fig_pie_2000, fig_pie_2025


@callback(
    Output('genre-selection-container', 'style'),
    Input('box-office-dropdown', 'value')


)
def show_hide_genre_select(auswahl):
    if auswahl == 'genres':
        return {'display': 'block'}
    return {'display': 'none'}



@callback(
    Output('box-office-graph', 'figure'),
    Input('box-office-dropdown', 'value'),
    Input('genre-multi-select', 'value') 
)
def update_box_office_chart(select, choosen_genre):
    if select == 'total':
        return plot_toal_boxoffice(data_2000, data_2025)
        
    elif select == 'genres':
    
        if not choosen_genre:
            return px.bar(title="Please select a genre to compare")
            
        return plot_genre_comp(
            dataframe_old=data_2000, 
            dataframe_new=data_2025, 
            genre_list=choosen_genre
        )

