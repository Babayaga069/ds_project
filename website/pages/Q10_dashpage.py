import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import plotly.express as px


dash.register_page(__name__, name='Question:10')

livedata_fantasy = pd.read_csv('pages/precomputed_fantasy.csv')
livedata_horror = pd.read_csv('pages/precomputed_horror.csv')

data_fantasy_cached = pd.read_csv('pages/fantasy_plotframe.csv')
data_horror_cached = pd.read_csv('pages/horror_plotframe.csv')


def wordmap(dataframe, title):
    frequency = dataframe.set_index('Plotphrase')['Count'].to_dict()

    wordmap = WordCloud(
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(frequency)

    figure = px.imshow(wordmap.to_array())
    figure.update_layout(
        title = f"Genre tropes for {title} movies",
        title_x = 0.5,
        xaxis = {'showgrid': False, 'showticklabels': False , 'zeroline': False},
        yaxis= {'showgrid': False, 'showticklabels': False , 'zeroline': False},
        hovermode = False,
        margin = dict(l=0, r= 0, t = 50 , b = 0)
    )
    return figure  

def boxplot(dataframe, column_box_office, genre):
    figure = px.box(
        dataframe,
        x = "Used_Plotphrases",
        y = column_box_office,
        color = "Used_Plotphrases",
        color_discrete_map = {False: '#ff9999', True: '#66b3ff'},
        category_orders= {"Used_Plotphrases": ["True","False"]}
    )
    figure.update_layout(
        title = f"Distribution of Box office for {genre} movies",
        title_font_size = 14,
        xaxis_title = "Using Common plotphrases?",
        yaxis_title = "Box office revenue in $"
    
    )
    return figure


def result_barcharts(dataframe, column_box_office):
    """
    Function that shows the the commeted line in the function above
    """
    count_data = dataframe['Used_Plotphrases'].value_counts().reset_index()
    count_data.columns = ['Used_Plotphrases', 'Count']
    count_data['Used_Plotphrases']  = count_data['Used_Plotphrases'].astype(str)

    figure_count = px.bar(
        count_data,
        x = "Used_Plotphrases",
        y = "Count",
        color = "Used_Plotphrases",
        title = "Count of Movies",
        labels = {'Used_Plotphrases': 'Plotphrase used?', 'Count': 'Count of Movies'},
        color_discrete_map = {'True': '#66b3ff', 'False': '#ff9999'},
        category_orders= {"Used_Plotphrases": ["True","False"]}
    )

    success_data = dataframe.groupby("Used_Plotphrases")[column_box_office].mean().reset_index()
    success_data.columns = ["Used_Plotphrases", "Average_Sucess"]
    success_data["Used_Plotphrases"] = success_data["Used_Plotphrases"].astype(str)

    figure_sucess = px.bar(
        success_data,
        x = "Used_Plotphrases",
        y = "Average_Sucess",
        color = "Used_Plotphrases",
        title = "Average Box office",
        labels = {'Used_Plotphrases': 'Plotphrase used?', 'Average_Success': 'Average Box office in $'},
        color_discrete_map = {'True': '#66b3ff', 'False': '#ff9999'},
        category_orders= {"Used_Plotphrases": ["True","False"]}

    )

    figure_sucess.update_layout(yaxis_tickformat =',.0f' )

    return figure_count, figure_sucess

#initial values
initial_threshold = 0.6
livedata_fantasy["Used_Plotphrases"] = (livedata_fantasy['Similarity_Score']>= initial_threshold).map({True:"True", False: "False"})

figure_wc_fantasy = wordmap(data_fantasy_cached, title= "Fantasy")
figure_boxplot_fantasy = boxplot(livedata_fantasy, column_box_office= "box_office_worldwide", genre = "Fantasy")
figure_bar_count_fantasy, figure_bar_sucess_fantasy = result_barcharts(livedata_fantasy, column_box_office="box_office_worldwide")


layout = html.Div([
    html.H2("Context:"),
    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua." 
    " At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, " \
    "consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. " \
    "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),
    html.H2("Choose for which genre you want to see wordcloud", style = {'textAlign' : 'left'}),

    dcc.RadioItems(
        id = "input-selection",
        options = [
            {'label': ' Fantasy', 'value': 'Fantasy'},
            {'label': ' Horror', 'value': 'Horror'}
        ],
        value = "Fantasy",
        inline = True,
        style = {'textAlign': 'left', 'marginBottom': '20px'}
    ),

    html.Div ([
        dcc.Graph(
            id="genre-wordmap",
            figure = figure_wc_fantasy,
            style={"display": "flex", "justifyContent": "left"}
        )
    ]),

    html.H3("Choose genre to analyse"),
    dcc.RadioItems(
        id="genre-selection",
        options=[
            {"label": "Fantasy", "value": "fantasy"},
            {"label": "Horror", "value": "horror"}
        ],
        value="fantasy",
        inline=True,
        style={'marginBottom': '20px', 'fontSize': '18px'}
    ),

    html.Label("Choose Similarity Threshold "),
    dcc.Slider(
        id="threshold-slider",
        min=0.1,
        max=1.0,
        step=0.05,
        value=0.6,
        marks={i/10: str(i/10) for i in range (1,11)},
    ),

    html.Button("Update Values", 
                id="start-button",
                n_clicks=0,
                style={"display": "block", "marginBottom": "20px", "marginTop": "20px", "padding": "10px", "fontSize": "16px"}),
                

    dcc.Loading(
        id="loading-bar-charts",
        type="default",
        children=html.Div([
            dcc.Graph(
                id="bar-count",
                figure = figure_bar_count_fantasy,
                style = {"display": "inline-block", "width": "50%"}),
            dcc.Graph(
                id="bar-success",
                figure = figure_bar_sucess_fantasy,
                style = {"display": "inline-block", "width": "50%"}),
                ])
    ),

    html.H2("Boxplot showing Box office", style={"textAlign": "left"}),

    dcc.Loading(
        id="loading-boxplot",
        type="default",
        children=html.Div([
            dcc.Graph(
                id="box_office_plot",
                figure= figure_boxplot_fantasy #dfault
            )
        ])
    ),
    html.H1("Take Away:"),
    html.P("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua." 
    " At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, " \
    "consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea " \
    "rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),


    ])
@callback(
        Output("genre-wordmap","figure"),
        Input("input-selection", "value")
)

def update_wordcloud(input):
    if input == "Horror":
        return wordmap(data_horror_cached,"Horror")
    elif input == "Fantasy":
        return wordmap(data_fantasy_cached,"Fantasy")



@callback(
    Output("bar-count", "figure"),
    Output("bar-success", "figure"),
    Output("box_office_plot","figure"),

    Input("start-button", "n_clicks"),

    State("threshold-slider","value"),
    State("genre-selection", "value"),

    prevent_initial_call = True
)

def run_analysis(n_clicks, threshold_value, choosen_genre):

    if n_clicks == 0 or n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update
    
    if choosen_genre == "fantasy":
        updated_dataframe = livedata_fantasy
        shown_titel = "Fantasy"
    
    elif choosen_genre == "horror":
        updated_dataframe = livedata_horror
        shown_titel = "Horror"
    
    else: 
        return dash.no_update, dash.no_update, dash.no_update
    
    updated_dataframe["Used_Plotphrases"] = (updated_dataframe["Similarity_Score"] >= threshold_value).map({True: "True", False: "False"})

    figure_count , figure_sucess = result_barcharts(updated_dataframe,"box_office_worldwide")
    figure_boxplot = boxplot(updated_dataframe, column_box_office= "box_office_worldwide", genre=shown_titel)

    return figure_count, figure_sucess, figure_boxplot

        







    




    