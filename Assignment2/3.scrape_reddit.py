import praw
import pandas as pd

# Set up Reddit API connection
reddit = praw.Reddit(
    client_id="qKNt_Z8cEszM3hzGnoiAdg",
    client_secret="dLwIHWp9Tx4Pgycbd-anGQCTD6uP6g",
    user_agent="RedditScraperBot/0.1 (by u/your_username)"
)

# Choose the subreddit with stocks
subreddit = reddit.subreddit("stocks")  

# Scraping top 100 posts from the 'hot' section
posts = []
for post in subreddit.hot(limit=100):  
    posts.append({
        "Title": post.title,
        "Upvotes": post.score,
        "Comments": post.num_comments,
        "URL": post.url,
        "Text": post.selftext
    })

# Convert to DataFrame
df = pd.DataFrame(posts)
df.to_csv("reddit_stocks.csv", index=False)
print("Scraping complete! Data saved as reddit_stocks.csv")
