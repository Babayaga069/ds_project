import pandas as pd
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util




sim_model = SentenceTransformer('all-MiniLM-L6-v2')

def precompute_scores(dataframe_untouched, dataframe_plotphrases, column_box_office, column_plotphrase, sim_model):
    """
    Helper function to create cached result for website.Based on functions form Notebook in the questionsfolder.  Created Entire function with help of LLM
    dataframe_untouched: Raw movie data
    dataframe_plotphrases: Pre calculated frame with calculated phrase and count
    column_box_office: name of box office colum
    column_plotphrase: name of plot column
    sim_model:used Model
    """
    df = dataframe_untouched[dataframe_untouched[column_box_office] > 0].copy()
    list_plotphrase = list(dataframe_plotphrases['Plotphrase'])
    top_embeddings = sim_model.encode(list_plotphrase)

    best_phrase_list = []
    best_score_list = []


    for movie_plot in enumerate(df[column_plotphrase]):
        
            
        best_phrase = "None"
        best_score = 0.0
        check_text = str(movie_plot)

        if len(check_text.strip()) > 0:
            sentences = sent_tokenize(check_text)
            if len(sentences) > 0:
                sentence_embeddings = sim_model.encode(sentences)
                hits = util.cos_sim(sentence_embeddings, top_embeddings)
                best_score = hits.max().item()
                max_idx = hits.argmax().item()
                phrase_idx = max_idx % hits.shape[1]
                best_phrase = list_plotphrase[phrase_idx]

        
        best_phrase_list.append(best_phrase)
        best_score_list.append(best_score)
    
    
    df['Best_Match_Phrase'] = best_phrase_list
    df['Similarity_Score'] = best_score_list
    
    return df


data_fantasy = pd.read_csv('pages/movies_plot_fantasy.csv')  
data_fantasy_cached = pd.read_csv('pages/fantasy_plotframe.csv')

data_horror = pd.read_csv('pages/movies_plot_horror.csv')
data_horror_cached = pd.read_csv('pages/horror_plotframe.csv')

precomputed_fantasy = precompute_scores(data_fantasy, data_fantasy_cached, "box_office_worldwide", "plot", sim_model)
precomputed_fantasy.to_csv('pages/q10/precomputed_fantasy.csv', index=False)

precomputed_horror = precompute_scores(data_horror, data_horror_cached, "box_office_worldwide", "plot", sim_model)
precomputed_horror.to_csv('pages/q10/precomputed_horror.csv', index=False)

