import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load enriched Reddit and CNN data
reddit_df = pd.read_csv("nvidia_praw_enriched.csv")
cnn_df = pd.read_csv("nvidia_cnn_bing_enriched.csv")

# Create topic-to-label mapping (adjust these based on your actual labels)
reddit_labels = {
    0: "stock, growth, reddit",
    1: "stock, company, intel",
    2: "market, high, stock",
    3: "ai, revenue, corz",
    4: "nvidia, stock, ai"
}
cnn_labels = {
    0: "nvidia, rtx, gpu",
    1: "nvidia, dgx, station",
    2: "nvidia, dlss, app",
    3: "dlss, nvidia, app",
    4: "nvidia, geforce, driver"
}

# Assign readable topic labels
reddit_df["topic_label"] = reddit_df["lda_topic"].map(reddit_labels)
cnn_df["topic_label"] = cnn_df["lda_topic"].map(cnn_labels)

# Group and calculate mean sentiment per topic
reddit_scores = reddit_df.groupby("topic_label")["gpt_score"].mean().rename("Reddit")
cnn_scores = cnn_df.groupby("topic_label")["gpt_score"].mean().rename("CNN")

# Merge scores
heatmap_df = pd.concat([reddit_scores, cnn_scores], axis=1)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_df, annot=True, cmap="coolwarm", center=0, linewidths=0.5)
plt.title("Average GPT Sentiment Score per Topic (Reddit vs CNN)")
plt.tight_layout()
plt.savefig("heatmap_topic_vs_sentiment.png")
plt.show()

