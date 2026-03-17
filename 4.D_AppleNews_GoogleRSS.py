import feedparser
import pandas as pd
import time

#  Keywords + Years to cover Apple across time
keywords = [
    "Apple stock", "iPhone", "Apple Watch", "MacBook",
    "AirPods", "Apple Vision Pro", "Tim Cook", "Apple M1 chip",
    "Apple earnings", "Apple innovation"
]
years = ["2020", "2021", "2022", "2023", "2024", "2025"]

#  Store all collected news
all_articles = []

for keyword in keywords:
    for year in years:
        query = f"{keyword} {year}"
        print(f"🔎 Fetching: {query}")
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            all_articles.append({
                "Title": entry.title,
                "Published": entry.published,
                "Link": entry.link,
                "Query": query,
                "Source": "GoogleNewsRSS"
            })

        time.sleep(5)  # prevent hitting request limit

#  Clean up
df_rss = pd.DataFrame(all_articles)
df_rss.drop_duplicates(subset=["Title", "Link"], inplace=True)
df_rss["Date"] = pd.to_datetime(df_rss["Published"], errors="coerce")
df_rss = df_rss.dropna(subset=["Date"])
df_rss = df_rss[["Title", "Source", "Link", "Date", "Query"]]
df_rss = df_rss.sort_values(by="Date", ascending=False)

#  Save
df_rss.to_csv("apple_google_news_rss.csv", index=False)
print(f"\n Saved {len(df_rss)} unique Google News RSS articles to 'apple_google_news_rss.csv'")
