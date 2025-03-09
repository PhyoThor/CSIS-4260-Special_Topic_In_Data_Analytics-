import pandas as pd
import openai
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import logging
from openai import OpenAIError  # Corrected import for error handling

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration
OPENAI_API_KEY = "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"  # Replace with your actual OpenAI API key
INPUT_FILE = "reddit_stocks.csv"
OUTPUT_FILE = "reddit_stocks_final.csv"
IMPORTANCE_THRESHOLD = 50  # Threshold for Positive/Negative labeling

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY  

# Download NLTK resources
nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to summarize text using OpenAI API
def summarize(text):
    """
    Summarize text using OpenAI's GPT-3.5 API.
    """
    if not isinstance(text, str) or text.strip() == "":
        return "No summary available"

    try:
        response = openai.chat.completions.create(  # Corrected OpenAI API format
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this Reddit post in one sentence."},
                {"role": "user", "content": text}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logging.error(f"API request failed: {e}")
        return "API Error"

# Function to calculate sentiment score
def calculate_sentiment(text):
    """
    Calculate sentiment score using NLTK's VADER.
    """
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return sia.polarity_scores(text)["compound"]

# Function to calculate importance score
def calculate_importance_score(row):
    """
    Calculate importance score based on upvotes, comments, and sentiment.
    """
    return (row["Upvotes"] * 0.5) + (row["Comments"] * 0.3) + (row["Sentiment"] * 100)

# Function to assign Positive/Negative label
def assign_label(importance_score):
    """
    Assign "Positive" or "Negative" label based on importance score.
    """
    return "Positive" if importance_score >= IMPORTANCE_THRESHOLD else "Negative"

# Main function to process the data
def process_data(input_file, output_file):
    """
    Process the Reddit data: summarize, analyze sentiment, calculate importance scores, and assign labels.
    """
    try:
        # Load data
        logging.info(f"Loading data from {input_file}...")
        df = pd.read_csv(input_file)

        # Validate DataFrame
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        required_columns = ["Text", "Upvotes", "Comments"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain these columns: {required_columns}")

        # Summarize text
        logging.info("Summarizing text using OpenAI API...")
        tqdm.pandas(desc="Summarizing")
        df["Summary"] = df["Text"].progress_apply(summarize)

        # Analyze sentiment
        logging.info("Analyzing sentiment...")
        tqdm.pandas(desc="Sentiment Analysis")
        df["Sentiment"] = df["Text"].progress_apply(calculate_sentiment)

        # Calculate importance score
        logging.info("Calculating importance scores...")
        df["Importance_Score"] = df.apply(calculate_importance_score, axis=1)

        # Assign Positive/Negative label
        logging.info("Assigning Positive/Negative labels...")
        df["Label"] = df["Importance_Score"].apply(assign_label)

        # Save results
        logging.info(f"Saving results to {output_file}...")
        df.to_csv(output_file, index=False)
        logging.info("Analysis complete!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Run the script
if __name__ == "__main__":
    process_data(INPUT_FILE, OUTPUT_FILE)
