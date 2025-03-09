import praw
import pandas as pd
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Set up Reddit API with a proper user agent
reddit = praw.Reddit(
    client_id="qKNt_Z8cEszM3hzGnoiAdg",  
    client_secret="dLwIHWp9Tx4Pgycbd-anGQCTD6uP6g", 
    user_agent="RedditScraperBot/0.1 (by u/your_username)"
)

# Scrape 100 Posts from the "technology" subreddit
subreddit = reddit.subreddit("technology")
posts = []  # List to store posts

for post in subreddit.hot(limit=100):
    posts.append([
        post.title, post.score, post.id, post.subreddit, 
        post.url, post.num_comments, post.selftext, post.created
    ])

# Convert scraped data into a DataFrame
df = pd.DataFrame(posts, columns=["title", "score", "id", "subreddit", "url", "num_comments", "body", "created"])
df.to_csv("reddit_technology.csv", index=False)
print("Scraping complete! Sample data:")
print(df.head(10))

# Summarization using `sumy`
def summarize_text(text, num_sentences=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

df["summary"] = df["body"].apply(lambda x: summarize_text(x) if len(x) > 50 else x)
print("Summarization complete! Sample summaries:")
print(df[["title", "summary"]].head(10))

# Sentiment Analysis using `VADER`
def get_vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['compound']  # Returns a compound score that combines all aspects

df['vader_sentiment'] = df['summary'].apply(get_vader_sentiment)
print("Vader Sentiment analysis complete! Sample scores:")
print(df[["title", "vader_sentiment"]].head(10))

# # Sentiment Analysis using `TextBlob`
# def get_sentiment(text):
#     return TextBlob(text).sentiment.polarity

# df["sentiment"] = df["summary"].apply(lambda x: get_sentiment(x))
# print("Sentiment analysis complete! Sample scores:")
# print(df[["title", "sentiment"]].head(10))

# Compute Importance Score including a label for direction based on sentiment
def compute_importance(text, upvotes, vader_sentiment):
    length_score = min(len(text) / 500, 1) * 50  # Up to 50 points based on text length
    upvote_score = min(upvotes / 100, 1) * 50    # Up to 50 points based on upvotes
    base_importance = length_score + upvote_score  # Total base importance (0 to 100)

    # Adjusting the calculation to avoid neutral by considering any non-zero sentiment as positive or negative
    if vader_sentiment != 0:
        directional_importance = base_importance * vader_sentiment
        importance_label = "Positive" if vader_sentiment > 0 else "Negative"
    else:
        # If sentiment is 0, arbitrarily assign a direction based on whether score or length is greater
        directional_importance = base_importance
        importance_label = "Positive" if upvote_score >= length_score else "Negative"

    return directional_importance, importance_label

df[['importance_score', 'importance_direction']] = df.apply(
    lambda row: compute_importance(row["body"], row["score"], row["vader_sentiment"]), axis=1, result_type='expand')

print("Importance scoring complete! Sample scores:")
print(df[["title", "importance_score", "importance_direction"]].head())

# Save & Display Processed Data
df.to_csv("reddit_analysis_results_vader.csv", index=False)
print("Analysis Complete!")
print(df[["title", "score", "id", "subreddit", "url", "num_comments", "body", "created"]].head(10))
