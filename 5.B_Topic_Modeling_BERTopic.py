# 1. Imports and data loading
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 2. Load preprocessed text
df = pd.read_csv("./.venv/data/apple_news_newsapi_rotated_cleaned.csv")
documents = df["clean_text"].dropna().tolist()

# 3. Prepare timestamps
df["Date"] = pd.to_datetime(df["PublishedAt"])

# 4. Fit BERTopic
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model, language="english", verbose=True)
topics, probs = topic_model.fit_transform(documents)

# 5. Save topics to dataframe
df["Topic"] = topics
df.to_csv("./.venv/data/apple_news_with_topics.csv", index=False)

# 6. Topic info + overview
print(topic_model.get_topic_info().head())

# 7. Compute topic trends over time
topics_over_time = topic_model.topics_over_time(df["clean_text"].tolist(), df["Date"].tolist())

# 8. Save interactive HTML
fig = topic_model.visualize_topics_over_time(topics_over_time)
fig.write_html("bertopic_topic_trends.html")

# 9. Clean topic trend DataFrame
df["Day"] = df["Date"].dt.date
trend_counts = df.groupby(["Day", "Topic"]).size().reset_index(name="Count")
trend_pivot = trend_counts.pivot(index="Day", columns="Topic", values="Count").fillna(0)
active_topics = trend_pivot.sum()[trend_pivot.sum() >= 3].index
filtered_trends = trend_pivot[active_topics]

# 10. Optional: plot trend
fig, ax = plt.subplots(figsize=(12,6))
filtered_trends.plot(figsize=(12,6), marker='o')

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.title("Topic Trends Over Time (Filtered)")
plt.xlabel("Date")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()
