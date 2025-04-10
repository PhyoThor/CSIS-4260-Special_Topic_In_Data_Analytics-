import yfinance as yf
import pandas as pd
from datetime import datetime

# Fetch AAPL news
ticker = yf.Ticker("AAPL")
news_data = ticker.news  # This returns a list of dictionaries

# Safely extract relevant info
clean_news = []
for article in news_data:
    content = article.get("content", {})
    if content:
        clean_news.append({
            "Title": content.get("title", ""),
            "Published": content.get("pubDate", ""),
            "Link": content.get("canonicalUrl", {}).get("url", ""),
            "Source": content.get("provider", {}).get("displayName", "Yahoo Finance"),
        })

# Convert to DataFrame
df_yahoo_news = pd.DataFrame(clean_news)

# Optional: Format date
df_yahoo_news["Published"] = pd.to_datetime(df_yahoo_news["Published"], errors="coerce")
df_yahoo_news = df_yahoo_news.dropna(subset=["Title", "Link"])

# Save or display
df_yahoo_news.to_csv("apple_yahoo_finance_news.csv", index=False)
print(f" Extracted {len(df_yahoo_news)} Yahoo Finance news articles for Apple.")
print(df_yahoo_news.head())
