import pandas as pd

# === Load News + Stock Files ===
news_path = ".venv/data/apple_google_news_with_summary.csv"
stock_path = ".venv/data/apple_stock_news_merged.csv"

# Load and convert dates
news_df = pd.read_csv(news_path, parse_dates=["Date"])
stock_df = pd.read_csv(stock_path, parse_dates=["Date"])

# Convert both to timezone-naive (drop timezone info)
news_df["Date"] = news_df["Date"].dt.tz_localize(None)
stock_df["Date"] = stock_df["Date"].dt.tz_localize(None)

# Sort by date for merge_asof to work
news_df = news_df.sort_values("Date")
stock_df = stock_df.sort_values("Date")

# Merge (asof: match nearest earlier date)
merged_df = pd.merge_asof(news_df, stock_df, on="Date", direction="backward")

# Drop rows with missing key features
merged_df = merged_df.dropna(subset=["Close", "RSI", "MACD"])

# Define target: 1 if price goes up tomorrow, else 0
merged_df["Target"] = (merged_df["Close"].pct_change().shift(-1) > 0).astype(int)

# Save final file
merged_df.to_csv("apple_news_stock_enriched.csv", index=False)
print(" Final enriched dataset saved: apple_news_stock_enriched.csv")
