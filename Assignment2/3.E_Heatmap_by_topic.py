import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(df_path, source_name, output_path):
    # Load the data
    df = pd.read_csv(df_path)

    # Check required columns
    if "lda_topic" not in df.columns or "gpt_score" not in df.columns:
        raise ValueError(f"Missing required columns in {source_name} data.")

    # Average score by topic
    topic_score = df.groupby("lda_topic")["gpt_score"].mean().reset_index()

    # If topic labels are available, map them
    if "topic_label" in df.columns:
        topic_score = topic_score.merge(
            df[["lda_topic", "topic_label"]].drop_duplicates(), 
            on="lda_topic", 
            how="left"
        )
        topic_score = topic_score.sort_values("lda_topic")
        topic_score.set_index("topic_label", inplace=True)
    else:
        topic_score = topic_score.sort_values("lda_topic")
        topic_score.set_index("lda_topic", inplace=True)

    # Plot heatmap
    plt.figure(figsize=(8, 5))
    sns.heatmap(topic_score.T, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=1)
    plt.title(f"🔥 Avg GPT Sentiment Score per Topic – {source_name}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Heatmap saved: {output_path}")

# Run for both Reddit and CNN
plot_heatmap("nvidia_praw_enriched.csv", "Reddit", "reddit_topic_sentiment_heatmap.png")
plot_heatmap("nvidia_cnn_bing_enriched.csv", "CNN", "cnn_topic_sentiment_heatmap.png")
