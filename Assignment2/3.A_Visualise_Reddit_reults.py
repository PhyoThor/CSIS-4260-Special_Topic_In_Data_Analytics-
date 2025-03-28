import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Load enriched Reddit data
df = pd.read_csv("nvidia_praw_enriched.csv")

# Ensure necessary columns exist
required_cols = ["gpt_score", "gpt_direction", "lda_topic", "keywords", "gpt_summary"]
if not all(col in df.columns for col in required_cols):
    raise ValueError("Missing one or more required columns in the dataset.")

topic_labels = {
    0: "stock, growth, reddit",
    1: "stock, company, intel",
    2: "market, high, stock",
    3: "ai, revenue, corz",
    4: "nvidia, stock, ai"
}

# --- 1. Sentiment Distribution Bar Chart ---
df["gpt_direction"].value_counts().plot(kind='bar', color=['green', 'red', 'gray'])
plt.title("Sentiment Direction Distribution (Reddit)")
plt.xlabel("Sentiment Direction")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reddit_sentiment_distribution.png")
plt.clf()

# --- 2. Histogram of GPT Scores ---
df["gpt_score"].plot(kind='hist', bins=20, color='skyblue', edgecolor='black')
plt.title("GPT Score Distribution (Reddit)")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("reddit_score_histogram.png")
plt.clf()

# --- 3. Average Score by Topic ---
df.groupby("lda_topic")["gpt_score"].mean().plot(kind='bar', color='purple')
plt.title("Average GPT Score per LDA Topic (Reddit)")
plt.xlabel("LDA Topic")
plt.ylabel("Average Score")
legend_labels = [f"{i} = {label}" for i, label in topic_labels.items()]
plt.legend(legend_labels, loc='best')
plt.tight_layout()
plt.savefig("reddit_avg_score_by_topic.png")
plt.clf()


# --- 4. Pie Chart of Direction ---
df["gpt_direction"].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['green', 'red', 'gray'])
plt.title("Sentiment Direction Proportion (Reddit)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("reddit_direction_pie.png")
plt.clf()

# --- 5. Word Cloud of Keywords ---
all_keywords = ' '.join(df["keywords"].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_keywords)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Keyword Word Cloud (Reddit)")
plt.tight_layout()
plt.savefig("reddit_wordcloud.png")
plt.clf()

# --- 6. Topic Frequency Bar Chart ---
df["topic_label"] = df["lda_topic"].map(topic_labels)
df["topic_label"].value_counts().plot(kind='bar', color='orange')
plt.title("LDA Topic Frequency (Reddit)")
plt.xlabel("Topic")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reddit_topic_frequency.png")
plt.clf()

# --- 7. Box Plot of Scores by Topic ---
df["topic_label"] = df["lda_topic"].map(topic_labels)
sns.boxplot(x="topic_label", y="gpt_score", data=df)
plt.title("GPT Score Distribution by Topic (Reddit)")
plt.xlabel("LDA Topic")
plt.ylabel("GPT Score")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("reddit_score_boxplot.png")
plt.clf()

# --- 8. Summary Length by Direction ---
df["summary_length"] = df["gpt_summary"].fillna("").apply(lambda x: len(x.split()))
df.groupby("gpt_direction")["summary_length"].mean().plot(kind='bar', color='teal')
legend_labels = [f"{i} = {label}" for i, label in topic_labels.items()]
plt.legend(legend_labels, loc='best')
plt.title("Average Summary Length by Sentiment Direction (Reddit)")
plt.xlabel("Direction")
plt.ylabel("Average Word Count")
plt.tight_layout()
plt.savefig("reddit_summary_length_by_direction.png")
plt.clf()

print("✅ Reddit visualizations saved!")
