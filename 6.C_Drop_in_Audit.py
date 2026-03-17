import pandas as pd
import matplotlib.pyplot as plt

# === LOAD DATA ===
news_path = ".venv/data/merged_apple_news_cleaned_full.csv"
stock_path = ".venv/data/apple_stock_news_merged.csv"

df_news = pd.read_csv(news_path, parse_dates=["Date"])
df_merged = pd.read_csv(stock_path, parse_dates=["Date"])

print("🔍 NEWS + STOCK DATA AUDIT\n")
df_news["Date"] = pd.to_datetime(df_news["Date"], errors="coerce")

# Filter for last 5 years only
cutoff = pd.Timestamp.today() - pd.DateOffset(years=5)
df_recent = df_news[df_news["Date"] >= cutoff].copy()

print("Rows in filtered df_recent:", len(df_recent))
print("Date range of full df_news:", df_news["Date"].min(), "→", df_news["Date"].max())

# Resample by month
monthly_counts = df_recent.resample("M", on="Date").size()

# === PLOT ===
plt.figure(figsize=(10, 6))
plt.plot(monthly_counts.index, monthly_counts.values, marker="o", color='dodgerblue', linewidth=2)

plt.title("\n Apple News Article Frequency (Last 5 Years)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Number of Articles")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()

# === BASIC STATS ===
print(f" Total Raw News (Cleaned): {len(df_news)}")
print(f" Total After Merging with Stock: {len(df_merged)}")
print(f" News Articles Dropped During Merge: {len(df_news) - len(df_merged)}\n")

# === NULL CHECKS ===
print(" Null Value Summary:")
print(df_news.isnull().sum(), "\n")

# === DUPLICATES ===
duplicates = df_news.duplicated(subset=["Title", "Date"]).sum()
print(f" Duplicate Title+Date Entries Removed: {duplicates}\n")

# === SOURCE DISTRIBUTION ===
print(" Article Sources (after cleaning):")
print(df_news["Source"].value_counts(), "\n")

# === TITLE QUALITY ===
df_news["Title Length"] = df_news["Title"].astype(str).str.len()
print(" Title Length Distribution:")
print(df_news["Title Length"].describe(), "\n")

# === GPT RELEVANCE FILTER (if present) ===
if "gpt_relevance_to_apple" in df_news.columns:
    print(" GPT Relevance to Apple:")
    print(df_news["gpt_relevance_to_apple"].value_counts(), "\n")

# === STOCK MERGE CHECK ===
missing_price = df_merged["Close"].isna().sum() if "Close" in df_merged.columns else "N/A"
print(f" Rows Missing Stock Price after Merge: {missing_price}\n")

# === OUTLIERS / ANOMALIES ===
print(" Date Anomalies:")
print(df_news[df_news["Date"] > pd.Timestamp.today()][["Title", "Date"]], "\n")

if "Close" in df_merged.columns:
    print(" Stock Price Zero Check:")
    print(df_merged[df_merged["Close"] == 0][["Date", "Close"]], "\n")

# === BUILD AUDIT SUMMARY DATAFRAME ===
audit_data = {
    "Metric": [
        "Total Raw News (Cleaned)",
        "Total After Merging with Stock",
        "News Articles Dropped During Merge",
        "Duplicate Title+Date Entries Removed",
        "Null Titles",
        "Null Dates",
        "Null Links",
        "Null Source",
        "Date Range Start",
        "Date Range End",
        "Most Common Source",
        "Least Common Source"
    ],
    "Value": [
        len(df_news),
        len(df_merged),
        len(df_news) - len(df_merged),
        df_news.duplicated(subset=["Title", "Date"]).sum(),
        df_news["Title"].isnull().sum(),
        df_news["Date"].isnull().sum(),
        df_news["Link"].isnull().sum(),
        df_news["Source"].isnull().sum(),
        df_news["Date"].min().strftime("%Y-%m-%d"),
        df_news["Date"].max().strftime("%Y-%m-%d"),
        df_news["Source"].value_counts().idxmax(),
        df_news["Source"].value_counts().idxmin()
    ]
}

audit_df = pd.DataFrame(audit_data)

# === SAVE AS CSV ===
output_path = "news_stock_audit_summary.csv"
audit_df.to_csv(output_path, index=False)
print(f"\n Audit summary saved to: {output_path}")

# ---------------------------------------------------------------------------------------------
# Figuring out why does the spike goes up only in 2024 and 2025
# Focus on recent surge (2024+)
df_news["YearMonth"] = df_news["Date"].dt.to_period("M")
spike_df = df_news[df_news["Date"] >= "2024-01-01"]

# Explode keywords from title
spike_words = spike_df["Title"].str.lower().str.findall(r'\b[a-z]{4,}\b').explode()

# Count top keywords
top_words = spike_words.value_counts().head(20)
top_titles = (
    spike_df["Title"]
    .value_counts()
)


import matplotlib.pyplot as plt

# Convert top keywords to DataFrame
keyword_table = top_words.reset_index()
keyword_table.columns = ["Keyword", "Frequency"]

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.axis('off')
tbl = plt.table(cellText=keyword_table.values,
                colLabels=keyword_table.columns,
                cellLoc='center',
                loc='center')

tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.2)

plt.title(" Top Keywords in 2024–2025", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("top_keywords_table_2024_2025.png", dpi=300)
plt.show()


headline_table = top_titles.reset_index()
headline_table.columns = ["Headline", "Count"]

# Optional: Truncate very long headlines
headline_table["Headline"] = headline_table["Headline"].apply(lambda x: x[:60] + "..." if len(x) > 60 else x)

fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
tbl = plt.table(cellText=headline_table.values,
                colLabels=headline_table.columns,
                cellLoc='left',
                loc='center')

tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1.1, 1.1)

plt.title("\n Most Repeated Headlines (2024–2025)", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("top_headlines_table_2024_2025.png", dpi=300, bbox_inches = 'tight')
plt.show()

# -------------------------------------------------------------------------------------
# Ensure date is parsed
df_news["Date"] = pd.to_datetime(df_news["Date"], errors="coerce")
df_news = df_news.dropna(subset=["Date"])

# Split periods
early_df = df_news[df_news["Date"].between("2020-01-01", "2021-12-31")]
spike_df = df_news[df_news["Date"] >= "2024-01-01"]

# Extract and count keywords
def get_top_keywords(df, top_n=10):
    words = df["Title"].str.lower().str.findall(r'\b[a-z]{4,}\b').explode()
    return words.value_counts().head(top_n)

top_early = get_top_keywords(early_df)
top_spike = get_top_keywords(spike_df)

# Combine into one DataFrame
df_keywords = pd.concat([
    top_early.rename("2020–2021"),
    top_spike.rename("2024–2025")
], axis=1).fillna(0)

# Sort by recent frequency
df_keywords = df_keywords.sort_values("2024–2025", ascending=True)


# Plot grouped horizontal bar chart
ax = df_keywords.plot(kind="barh", figsize=(10, 6), width=0.7)
plt.title("🔑 Keyword Comparison: 2020–2021 vs. 2024–2025")
plt.xlabel("Frequency")
plt.grid(axis="x")
plt.tight_layout()
plt.legend(title="Period")
plt.show()
