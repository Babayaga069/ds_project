import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util

dash.register_page(__name__, name='Question:10')

data_fantasy = pd.read_csv('pages/movies_plot_fantasy.csv')
data_horror = pd.read_csv('pages/movies_plot_horror.csv')

data_fantasy_cached = pd.read_csv('pages/fantasy_plotframe.csv')
data_horror_cached = pd.read_csv('pages/horror_plotframe.csv')

sim_model = SentenceTransformer('all-MiniLM-L6-v2')

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
        y = "box_office_worldwide",
        color = "Used_Plotphrases",
        color_discrete_map = {False: '#ff9999', True: '#66b3ff'}
    )
    figure.update_layout(
        title = f"Distribution of Box office for {genre} movies",
        title_font_size = 14,
        xaxis_title = "Using Common plotphrases?",
        yaxis_title = "Box office revenue in $"
    )
    return figure

def compare_movies_with_plotphrases(dataframe_untouched, dataframe_plotphrases, column_box_office, column_plotphrase, sim_model, threshold):

    dataframe_untouched = dataframe_untouched[dataframe_untouched[column_box_office] > 0]
    list_plotphrase = list(dataframe_plotphrases['Plotphrase'])
    top_embeddings = sim_model.encode(list_plotphrase)

    phrase_used_list = []
    best_phrase_list = []
    best_score_list = []

    for movie_plot in dataframe_untouched[column_plotphrase]:
        
        #default values

        movies_uses_plotphrase = False
        best_phrase = "None"
        best_score = 0.0
        check_text = str(movie_plot)

        if len(check_text.strip()) > 0:

            sentences = sent_tokenize(check_text)

            if len(sentences) > 0 :

                sentence_embeddings = sim_model.encode(sentences)
                hits = util.cos_sim(sentence_embeddings, top_embeddings)
                best_score = hits.max().item()
                max_idx= hits.argmax().item()
                phrase_idx = max_idx % hits.shape[1]
                best_phrase = list_plotphrase[phrase_idx]

                if best_score >= threshold:
                    movies_uses_plotphrase = True

        phrase_used_list.append(movies_uses_plotphrase)
        best_phrase_list.append(best_phrase)
        best_score_list.append(best_score)
    
    dataframe_untouched['Used_Plotphrases'] = phrase_used_list
    dataframe_untouched['Best_Match_Phrase'] = best_phrase_list
    dataframe_untouched['Similarity_Score'] = best_score_list

    #  #debugging
    # csv_filename = 'movies_debug.csv'
    # dataframe_untouched.to_csv(csv_filename, index=False, sep=';', encoding='utf-8')
    # print(f"Create debug file: {csv_filename}")

    # # Print result 
    # count_movie = dataframe_untouched['Used_Plotphrases'].value_counts()
    # print("Movies used Plot")
    # print(count_movie)
    # succes = dataframe_untouched.groupby('Used_Plotphrases')[column_box_office].mean()
    # succes_readable = succes.apply(lambda x: f"{x:,.0f} $")
    # print("")
    # print("Average Sucess:")
    # print(succes_readable)

    return dataframe_untouched

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
        color_discrete_map = {'True': '#66b3ff', 'False': '#ff9999'} 
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
        color_discrete_map = {'True': '#66b3ff', 'False': '#ff9999'}

    )

    figure_sucess.update_layout(yaxis_tickformat =',.0f' )

    return figure_count, figure_sucess

figure_wc_fantasy = wordmap(
    data_fantasy_cached,
    title = "Fantasy"
)

figure_wc_horror = wordmap(
    data_horror_cached,
    title="Horror"
)

livedata_fantasy = compare_movies_with_plotphrases(
    data_fantasy,
    data_fantasy_cached,
    column_box_office = "box_office_worldwide",
    column_plotphrase = "plot",
    sim_model = sim_model,
    threshold = 0.5

)

livedata_horror = compare_movies_with_plotphrases(
    data_horror,
    data_horror_cached,
    column_box_office = "box_office_worldwide",
    column_plotphrase = "plot",
    sim_model = sim_model,
    threshold = 0.5
)

figure_boxplot_fantasy = boxplot(
    livedata_fantasy,
    column_box_office= "box_office_worldwide",
    genre = "Fantasy"
)

figure_boxplot_horror = boxplot(
    livedata_horror,
    column_box_office = "box_office_worldwide",
    genre= "Horror"
)

figure_bar_count_fantasy, figure_bar_sucess_fantasy = result_barcharts(
    livedata_fantasy, 
    column_box_office='box_office_worldwide')
figure_bar_count_horror, figure_bar_sucess_horror = result_barcharts(
    livedata_horror,
    column_box_office='box_office_worldwide')
    

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

    html.Label("Choose Similarity Threshold (The higher the stricter)(Updates take around 20-30 seconds)"),
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
        data_genre = data_fantasy
        data_plot = data_fantasy_cached
        shown_titel = "Fantasy"

    elif choosen_genre == "horror":
        data_genre = data_horror
        data_plot = data_horror_cached
        shown_titel = "Horror"

    else:
        return dash.no_update, dash.no_update, dash.no_update
    
    updated_dataframe= compare_movies_with_plotphrases(
        dataframe_untouched= data_genre,
        dataframe_plotphrases= data_plot,
        column_box_office="box_office_worldwide",
        column_plotphrase= "plot",
        sim_model= sim_model,
        threshold= threshold_value
    )
    
    figure_count , figure_success = result_barcharts(updated_dataframe, "box_office_worldwide")
    figure_boxplot = boxplot(updated_dataframe, column_box_office="box_office_worldwide", genre=shown_titel)

    return figure_count, figure_success, figure_boxplot
    

        







    




    