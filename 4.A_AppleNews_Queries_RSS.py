import feedparser
import pandas as pd
import time

# Define base search terms and years for coverage
keywords = [
    "apple stock",
    "apple earnings",
    "apple iphone",
    "apple macbook",
    "apple watch",
    "apple airpods",
    "apple vision pro",
    "apple M1 chip",
    "apple services revenue",
    "tim cook"
]

years = ["2020", "2021", "2022", "2023", "2024", "2025"]

# Collect articles here
all_articles = []

# Rotate through combinations of keyword + year
for keyword in keywords:
    for year in years:
        query = f"{keyword} {year}"
        print(f"🔎 Fetching: {query}")

        # Format Google News RSS URL
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)

        # Extract news entries
        for entry in feed.entries:
            all_articles.append({
                "Title": entry.title,
                "Published": entry.published,
                "Link": entry.link,
                "Query": query
            })
        
        # Gentle pause to avoid suspicion
        time.sleep(5)

#  Clean & structure
df_news = pd.DataFrame(all_articles)
df_news.drop_duplicates(subset=["Title", "Link"], inplace=True)
df_news["Published"] = pd.to_datetime(df_news["Published"], errors="coerce")
df_news = df_news.dropna(subset=["Published"])
df_news = df_news.sort_values(by="Published", ascending=False)

# Save to CSV
df_news.to_csv("apple_news_rotated.csv", index=False)

print(f"\n Finished! {len(df_news)} unique articles saved to 'apple_news_rotated.csv'")
