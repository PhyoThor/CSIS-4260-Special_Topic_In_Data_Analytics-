# scrape_praw.py

import praw
import pandas as pd
from datetime import datetime
import time
start_time = time.time()

# Initialize PRAW with your credentials
reddit = praw.Reddit(
    client_id="qKNt_Z8cEszM3hzGnoiAdg",
    client_secret="dLwIHWp9Tx4Pgycbd-anGQCTD6uP6g",
    user_agent="RedditScraperBot/0.1 (by u/your_username)"
)

# Search query
query = "Nvidia OR NVDA"
subreddit = reddit.subreddit("stocks+wallstreetbets+investing")

# Parameters
limit = 100  # You can adjust this
posts = []

# Scrape data
for post in subreddit.search(query, sort="new", limit=limit):
    posts.append({
        "id": post.id,
        "title": post.title,
        "selftext": post.selftext,
        "score": post.score,
        "created_utc": datetime.fromtimestamp(post.created_utc),
        "subreddit": post.subreddit.display_name,
        "url": post.url
    })

# Convert to DataFrame
df = pd.DataFrame(posts)

# Save to CSV
df.to_csv("nvidia_praw_posts.csv", index=False)
print(f"Saved {len(df)} posts to nvidia_praw_posts.csv")
end_time = time.time()
duration = end_time - start_time
print(f" Saved {len(df)} Reddit posts in {duration:.2f} seconds")