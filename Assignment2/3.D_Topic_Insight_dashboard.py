import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load enriched files
reddit_df = pd.read_csv("nvidia_praw_enriched.csv")
cnn_df = pd.read_csv("nvidia_cnn_bing_enriched.csv")

# ----------- Define Topic Labels ----------- #
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

# ----------- Apply Mapping ----------- #
reddit_df["topic_label"] = reddit_df["lda_topic"].map(reddit_labels)
cnn_df["topic_label"] = cnn_df["lda_topic"].map(cnn_labels)

# ------------- Mean Sentiment Score (for Heatmap) -------------
reddit_mean = reddit_df.groupby("topic_label")["gpt_score"].mean().rename("Reddit_Score")
cnn_mean = cnn_df.groupby("topic_label")["gpt_score"].mean().rename("CNN_Score")
heatmap_df = pd.concat([reddit_mean, cnn_mean], axis=1)
heatmap_df.to_csv("heatmap_topic_sentiment.csv")

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_df, annot=True, cmap="coolwarm", center=0)
plt.title(" Average GPT Sentiment Score per Topic")
plt.tight_layout()
plt.savefig("heatmap_topic_sentiment.png")
plt.clf()

# ------------- Standard Deviation (Volatility) -------------
reddit_std = reddit_df.groupby("topic_label")["gpt_score"].std().rename("Reddit_Std")
cnn_std = cnn_df.groupby("topic_label")["gpt_score"].std().rename("CNN_Std")
std_df = pd.concat([reddit_std, cnn_std], axis=1)
std_df.to_csv("topic_sentiment_std.csv")

# ------------- Topic Frequency (Post Count) -------------
reddit_freq = reddit_df["topic_label"].value_counts().rename("Reddit_Frequency")
cnn_freq = cnn_df["topic_label"].value_counts().rename("CNN_Frequency")
freq_df = pd.concat([reddit_freq, cnn_freq], axis=1)
freq_df.to_csv("topic_frequency.csv")

plt.figure(figsize=(10, 6))
sns.heatmap(freq_df.fillna(0), annot=True, cmap="YlGnBu", fmt=".0f")
plt.title(" Post Frequency per Topic (Reddit vs CNN)")
plt.tight_layout()
plt.savefig("heatmap_topic_frequency.png")
plt.clf()

# ------------- Directional Bias (%) -----------------
def direction_distribution(df, label):
    dist = df.groupby("topic_label")["gpt_direction"].value_counts(normalize=True).unstack().fillna(0)
    dist.columns = [f"{label}_{col}" for col in dist.columns]
    return dist

reddit_dir = direction_distribution(reddit_df, "Reddit")
cnn_dir = direction_distribution(cnn_df, "CNN")
dir_dist = pd.concat([reddit_dir, cnn_dir], axis=1)
dir_dist.to_csv("topic_direction_distribution.csv")

# ------------- Merge Everything into One Dashboard CSV -------------
dashboard_df = pd.concat([heatmap_df, std_df, freq_df, dir_dist], axis=1)
dashboard_df.to_csv("topic_analysis_dashboard.csv")

print(" All topic-level insight metrics saved successfully!")
