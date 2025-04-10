import requests
import pandas as pd
import time

# Your NewsAPI key
NEWSAPI_KEY = "3359a528b4f74fe4be6dd3c870759dac"  

# Define Apple-related search terms
queries = [
    "Apple Inc", "Apple stock", "iPhone", "MacBook", "Apple Watch", 
    "Apple earnings", "Apple Vision Pro", "AirPods", "Apple M1 Chip" ,"Tim Cook", "iOS update"
]

def fetch_newsapi_articles(query, pages=3):
    """Fetches articles for a single query from NewsAPI."""
    articles = []
    base_url = "https://newsapi.org/v2/everything"

    for page in range(1, pages + 1):
        print(f"🔎 {query} | Page {page}")
        
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "page": page,
            "apiKey": NEWSAPI_KEY
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            print(f" Error for query '{query}': {data.get('message', 'Unknown error')}")
            break

        for item in data["articles"]:
            articles.append({
                "Query": query,
                "Title": item.get("title"),
                "Description": item.get("description"),
                "PublishedAt": item.get("publishedAt"),
                "Source": item.get("source", {}).get("name"),
                "URL": item.get("url")
            })

        time.sleep(12)  

    return articles

# Run all queries and collect results
all_articles = []
for q in queries:
    all_articles.extend(fetch_newsapi_articles(q, pages=5))  # 5 pages max

# Clean & deduplicate
df_all = pd.DataFrame(all_articles)
df_all["PublishedAt"] = pd.to_datetime(df_all["PublishedAt"])
df_all.drop_duplicates(subset=["Title", "URL"], inplace=True)

# Save
df_all.to_csv("apple_news_newsapi_rotated.csv", index=False)
print(f"\ Done! Collected {len(df_all)} unique articles from NewsAPI.")
