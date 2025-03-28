import pandas as pd
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# --------- Initialize KeyBERT Model ------------- #
model = SentenceTransformer('all-MiniLM-L6-v2')
kw_model = KeyBERT(model=model)

# -------- Keyword Extraction Function ---------- #
def extract_keywords(text, top_n=5):
    if not isinstance(text, str) or text.strip() == '':
        return []
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n
    )
    return [kw[0] for kw in keywords]

# -------------- Processing Function ----------------- #
def keyword_pipeline(input_file, output_file, source):
    print(f"\n🔑 Extracting keywords for {source}...")
    df = pd.read_csv(input_file)
    df['keywords'] = df['clean_text'].fillna('').apply(lambda x: extract_keywords(x, top_n=5))
    df.to_csv(output_file, index=False)
    print(f" Saved with keywords: {output_file}")

# --------------- Run for Both Sources --------------- #
if __name__ == "__main__":
    keyword_pipeline("nvidia_praw_topic_labeled.csv", "nvidia_praw_keywords.csv", source="Reddit")
    keyword_pipeline("nvidia_cnn_bing_topic_labeled.csv", "nvidia_cnn_bing_keywords.csv", source="CNN")
