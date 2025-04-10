import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the dataset
df = pd.read_csv(".venv/data/merged_apple_news_cleaned_full.csv")

# Convert 'Date' to datetime and drop rows with invalid dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# Extract year-month for grouping
df["YearMonth"] = df["Date"].dt.to_period("M")

# Function to extract clean keywords (3+ letter words)
def extract_keywords(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', str(text))  # 3+ letter alphabetic words
    return words

# Apply keyword extraction
df["Keywords"] = df["Title"].apply(extract_keywords)

# Explode keywords for monthly aggregation
monthly_keywords = (
    df.explode("Keywords")
      .groupby(["YearMonth", "Keywords"])
      .size()
      .reset_index(name="Count")
)

# Get top N keywords overall
top_n = 10
top_keywords = (
    monthly_keywords.groupby("Keywords")["Count"].sum()
    .sort_values(ascending=False)
    .head(top_n)
    .index.tolist()
)

# Filter and pivot for plotting
filtered = monthly_keywords[monthly_keywords["Keywords"].isin(top_keywords)]
pivot_df = filtered.pivot(index="YearMonth", columns="Keywords", values="Count").fillna(0)

# Plotting trends
plt.figure(figsize=(14, 6))
pivot_df.plot(marker='o')
plt.title(" Top 10 Keyword Trends Over Time")
plt.ylabel("Keyword Count")
plt.xlabel("Year-Month")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title="Keyword", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()
