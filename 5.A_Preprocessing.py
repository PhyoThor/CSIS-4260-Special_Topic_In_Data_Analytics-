import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

#Load the data
newsapi_df = pd.read_csv("./.venv/data/apple_news_newsapi_rotated.csv")

# Combine Title and Description into one field
newsapi_df["text"] = newsapi_df["Title"].fillna('') + " " + newsapi_df["Description"].fillna('')

# Use scikit-learn's stopword list
stop_words = ENGLISH_STOP_WORDS

# Updated preprocessing function (no lemmatization)
def preprocess_text_sklearn(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return " ".join(tokens)

# Apply preprocessing
newsapi_df["clean_text"] = newsapi_df["text"].apply(preprocess_text_sklearn)

print(newsapi_df[["text", "clean_text"]].head())
newsapi_df.to_csv("./.venv/data/apple_news_newsapi_rotated_cleaned.csv", index=False)