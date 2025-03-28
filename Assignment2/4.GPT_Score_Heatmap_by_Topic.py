import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load enriched datasets ---
df_reddit = pd.read_csv("nvidia_praw_enriched.csv")
df_cnn = pd.read_csv("nvidia_cnn_bing_enriched.csv")

# --- Load topic label mappings ---
reddit_topic_map = pd.read_csv("reddit_topic_labels.csv")
cnn_topic_map = pd.read_csv("cnn_topic_labels.csv")

# --- Convert to dictionary ---
reddit_topic_labels = dict(zip(reddit_topic_map["topic_id"], reddit_topic_map["label"]))
cnn_topic_labels = dict(zip(cnn_topic_map["topic_id"], cnn_topic_map["label"]))

# --- Map topic_label columns ---
df_reddit["topic_label"] = df_reddit["lda_topic"].map(reddit_topic_labels)
df_cnn["topic_label"] = df_cnn["lda_topic"].map(cnn_topic_labels)

# --- Add source info ---
df_reddit["source"] = "Reddit"
df_cnn["source"] = "CNN"

# --- Combine both ---
df_all = pd.concat([df_reddit, df_cnn], ignore_index=True)

# --- Pivot table: Average GPT Score per Topic per Source ---
heatmap_data = df_all.pivot_table(
    values="gpt_score",
    index="topic_label",
    columns="source",
    aggfunc="mean"
)

# --- Plot ---
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", center=0)
plt.title("📊 Average GPT Score by Topic and Source")
plt.xlabel("Source")
plt.ylabel("LDA Topic Label")
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("heatmap_topic_vs_score.png")
plt.show()
