import pandas as pd
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# --------------- Shared Utilities --------------- #

def tokenize(text):
    """Simple whitespace tokenizer."""
    return [word for word in str(text).lower().split() if word.isalpha()]

def run_lda(df, source_name, output_file, num_topics=5):
    print(f"\n Running LDA for {source_name}...")
    
    # Tokenize
    df['tokens'] = df['clean_text'].fillna('').apply(tokenize)
    
    # Create dictionary and corpus
    dictionary = corpora.Dictionary(df['tokens'])
    corpus = [dictionary.doc2bow(text) for text in df['tokens']]
    
    # Train LDA model
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=10)

    # Show topics
    print(f"\n Top {num_topics} topics in {source_name}:")
    for idx, topic in lda_model.print_topics(num_words=6):
        print(f"Topic {idx}: {topic}")
    
    # Assign dominant topic to each entry
    def get_dominant_topic(doc_bow):
        topic_probs = lda_model.get_document_topics(doc_bow)
        if topic_probs:
            top_topic = max(topic_probs, key=lambda x: x[1])
            return top_topic[0]
        return None

    df['lda_topic'] = [get_dominant_topic(doc) for doc in corpus]
    
    # Create readable topic labels
    topic_labels = {}
    for idx, topic in lda_model.print_topics(num_words=3):  # adjust num_words if needed
        words = topic.split('+')
        keywords = ', '.join([w.split('*')[1].strip().strip('"') for w in words])
        topic_labels[idx] = f"Topic {idx}: {keywords}"

    df["topic_label"] = df["lda_topic"].map(topic_labels)
    print(f"\n Topic Labels:")
    print(topic_labels)
    # Save topic_labels to CSV after printing
    label_filename = f"{source_name.lower()}_topic_labels.csv"
    pd.DataFrame(list(topic_labels.items()), columns=["topic_id", "label"]).to_csv(label_filename, index=False)
    print(f"📁 Saved topic labels to: {label_filename}")

    # Map topic labels into new column
    df["topic_label"] = df["lda_topic"].map(topic_labels)

    # Save to new file
    df.to_csv(output_file, index=False)
    print(f" Saved: {output_file}")

# --------------- Run for Both Sources --------------- #

# Reddit
df_reddit = pd.read_csv("nvidia_praw_clean.csv")
run_lda(df_reddit, source_name="Reddit", output_file="nvidia_praw_topic_labeled.csv")

# CNN
df_cnn = pd.read_csv("nvidia_cnn_bing_clean.csv")
run_lda(df_cnn, source_name="CNN", output_file="nvidia_cnn_bing_topic_labeled.csv")
