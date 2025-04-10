import pandas as pd
import os

# Define file paths
stock_path = "./.venv/data/apple_stock_with_indicators.csv"
news_path = "./.venv/data/merged_apple_news_cleaned_full.csv"
output_path = "./.venv/data/apple_stock_news_merged.csv"

# Load stock and news data
df_stock = pd.read_csv(stock_path)
df_news = pd.read_csv(news_path)

# Parse datetime fields with UTC-aware handling
df_stock["Date"] = pd.to_datetime(df_stock["Date"],format='mixed', utc=True)
df_news["Date"] = pd.to_datetime(df_news["Date"], format='mixed', utc=True)

# Sort both datasets by date for asof merge
df_stock_sorted = df_stock.sort_values("Date")
df_news_sorted = df_news.sort_values("Date")

# Perform merge_asof to align nearest past stock price to news date
df_merged = pd.merge_asof(
    df_news_sorted,
    df_stock_sorted,
    on="Date",
    direction="backward"
)

# Save merged dataset
df_merged.to_csv(output_path, index=False)
print(f" Merged dataset saved to: {output_path}")

# Display preview
print("\n Merged Data Preview:")
print(df_merged.head())
