# 1.F_clean_all.py

import pandas as pd
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Text cleaning function using spaCy
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    doc = nlp(text)
    cleaned = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(cleaned)

# Clean Reddit
df_reddit = pd.read_csv("nvidia_praw_posts.csv")
df_reddit['combined_text'] = df_reddit['title'].fillna('') + ' ' + df_reddit['selftext'].fillna('')
df_reddit['clean_text'] = df_reddit['combined_text'].apply(clean_text)
df_reddit.to_csv("nvidia_praw_clean.csv", index=False)
print("Reddit cleaned nvidia_praw_clean.csv")

# Clean CNN
df_cnn = pd.read_csv("nvidia_cnn_bing.csv")
df_cnn['combined_text'] = df_cnn['title'].fillna('') + ' ' + df_cnn['snippet'].fillna('')
df_cnn['clean_text'] = df_cnn['combined_text'].apply(clean_text)
df_cnn.to_csv("nvidia_cnn_bing_clean.csv", index=False)
print("CNN cleaned nvidia_cnn_bing_clean.csv")
