import pandas as pd
import matplotlib.pyplot as plt

# === LOAD DATA ===
news_path = ".venv/data/merged_apple_news_cleaned_full.csv"
stock_path = ".venv/data/apple_stock_news_merged.csv"

df_news = pd.read_csv(news_path, parse_dates=["Date"])


# === PREPARE DATA ===
df_news["Date"] = pd.to_datetime(df_news["Date"], errors="coerce")
df_news = df_news.dropna(subset=["Date"])
df_news["YearMonth"] = df_news["Date"].dt.to_period("M")

# Define time periods
early_df = df_news[df_news["Date"].between("2020-01-01", "2021-12-31")]
spike_df = df_news[df_news["Date"] >= "2024-01-01"]

# === HELPER FUNCTION ===
def get_top_keywords(df, top_n=20):
    words = df["Title"].str.lower().str.findall(r'\b[a-z]{4,}\b').explode()
    return words.value_counts().head(top_n)

# === TOP KEYWORDS: SPIKE PERIOD ===
top_keywords_spike = get_top_keywords(spike_df)

# === TOP TITLES: SPIKE PERIOD ===
top_titles = spike_df["Title"].value_counts().head(20).reset_index()
top_titles.columns = ["Headline", "Count"]
top_titles["Headline"] = top_titles["Headline"].apply(lambda x: x[:60] + "..." if len(x) > 60 else x)

# === DISPLAY TABLE: TOP KEYWORDS ===
fig, ax = plt.subplots(figsize=(6, 6))
ax.axis('off')
tbl = plt.table(cellText=top_keywords_spike.reset_index().values,
                colLabels=["Keyword", "Frequency"],
                cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.2)
plt.title("🔑 Top Keywords in 2024–2025", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("top_keywords_table_2024_2025.png", dpi=300)
plt.show()

# === DISPLAY TABLE: TOP HEADLINES ===
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
tbl = plt.table(cellText=top_titles.values,
                colLabels=["Headline", "Count"],
                cellLoc='left', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1.1, 1.1)
plt.title("📢 Most Repeated Headlines (2024–2025)", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("top_headlines_table_2024_2025.png", dpi=300, bbox_inches='tight')
plt.show()

# === COMPARE TOP KEYWORDS (2020–2021 vs 2024–2025) ===
top_keywords_early = get_top_keywords(early_df, top_n=20)

# Combine into comparison DataFrame
df_keyword_compare = pd.concat([
    top_keywords_early.rename("2020–2021"),
    top_keywords_spike.rename("2024–2025")
], axis=1).fillna(0)

# Sort by recent frequency
df_keyword_compare = df_keyword_compare.sort_values("2024–2025", ascending=True)

# === COMPARISON BAR CHART ===
ax = df_keyword_compare.plot(kind="barh", figsize=(10, 6), width=0.7, color=["skyblue", "salmon"])
plt.title("🔍 Keyword Comparison: 2020–2021 vs. 2024–2025", fontsize=14)
plt.xlabel("Frequency")
plt.grid(axis="x")
plt.tight_layout()
plt.legend(title="Period")
plt.savefig("keyword_comparison_2020_vs_2024.png", dpi=300)
plt.show()
