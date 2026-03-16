import pandas as pd
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util

print("Lade Modell...")


sim_model = SentenceTransformer('all-MiniLM-L6-v2')

def precompute_scores(dataframe_untouched, dataframe_plotphrases, column_box_office, column_plotphrase, sim_model):
    df = dataframe_untouched[dataframe_untouched[column_box_office] > 0].copy()
    list_plotphrase = list(dataframe_plotphrases['Plotphrase'])
    top_embeddings = sim_model.encode(list_plotphrase)

    best_phrase_list = []
    best_score_list = []

    print(f"Berechne {len(df)} Filme...")
    for index, movie_plot in enumerate(df[column_plotphrase]):
        if index % 100 == 0 and index > 0:
            print(f"Fortschritt: {index} / {len(df)} Filme berechnet...")
            
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

        # --- WICHTIG: Diese beiden Zeilen müssen IN der for-Schleife stehen ---
        # Sie müssen exakt unter dem "if len(check_text.strip()) > 0:" eingerückt sein!
        best_phrase_list.append(best_phrase)
        best_score_list.append(best_score)
    
    # --- WICHTIG: Diese beiden Zeilen stehen AUSSERHALB der for-Schleife ---
    # Sie werden erst ganz am Ende ausgeführt, wenn die Liste 1124 Einträge hat.
    df['Best_Match_Phrase'] = best_phrase_list
    df['Similarity_Score'] = best_score_list
    
    return df
print("Lade CSV Dateien...")
data_fantasy = pd.read_csv('pages/movies_plot_fantasy.csv')  # <-- Hier muss die originale Datei stehen!
data_fantasy_cached = pd.read_csv('pages/fantasy_plotframe.csv')

data_horror = pd.read_csv('pages/movies_plot_horror.csv')
data_horror_cached = pd.read_csv('pages/horror_plotframe.csv')

# 2. Fantasy berechnen und speichern
print("Starte Fantasy...")
precomputed_fantasy = precompute_scores(data_fantasy, data_fantasy_cached, "box_office_worldwide", "plot", sim_model)
precomputed_fantasy.to_csv('pages/precomputed_fantasy.csv', index=False)

# 3. Horror berechnen und speichern
print("Starte Horror...")
precomputed_horror = precompute_scores(data_horror, data_horror_cached, "box_office_worldwide", "plot", sim_model)
precomputed_horror.to_csv('pages/precomputed_horror.csv', index=False)

print("Fertig! Die Dateien precomputed_fantasy.csv und precomputed_horror.csv wurden erstellt.")