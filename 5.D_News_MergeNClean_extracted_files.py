import pandas as pd

# File paths (reloaded due to kernel reset)
files = {
    "Google RSS": ".venv/data/apple_google_news_rss.csv",
    "Google Custom": ".venv/data/apple_news_rotated.csv",
    "NewsAPI": ".venv/data/apple_news_newsapi_rotated.csv",
    "Yahoo Finance": ".venv/data/apple_yahoo_finance_news.csv"
}
# Reload and fix column inconsistencies
corrected_dataframes = []

for source, path in files.items():
    df = pd.read_csv(path)

    # Rename relevant columns to match standard schema
    if "PublishedAt" in df.columns:
        df.rename(columns={"PublishedAt": "Date", "URL": "Link"}, inplace=True)
    elif "Published" in df.columns:
        df.rename(columns={"Published": "Date"}, inplace=True)

    # Standardize columns: keep only necessary ones
    expected_columns = ["Title", "Date", "Link"]
    df = df[[col for col in expected_columns if col in df.columns]]
    df["Source"] = source

    # Parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    corrected_dataframes.append(df)

# Merge, clean, and save
df_merged_fixed = pd.concat(corrected_dataframes, ignore_index=True)
df_merged_fixed.drop_duplicates(subset=["Title", "Date"], inplace=True)
df_merged_fixed.dropna(subset=["Title", "Date", "Link"], inplace=True)

# Save the fully merged and cleaned file
merged_fixed_path = ".venv/data/merged_apple_news_cleaned_full.csv"
df_merged_fixed.to_csv(merged_fixed_path, index=False)





# # Standard columns to keep
# standard_columns = ["Title", "Snippet", "Date", "Link", "Source"]

# # Function to load and standardize each dataset
# def load_and_standardize(filepath, source_name):
#     try:
#         df = pd.read_csv(filepath)
#         df.columns = df.columns.str.strip()  # Clean column names
#         df["Source"] = source_name

#         # Standardize expected column names
#         if "summary" in df.columns:
#             df.rename(columns={"summary": "Snippet"}, inplace=True)
#         if "published" in df.columns:
#             df.rename(columns={"published": "Date"}, inplace=True)
#         if "link" in df.columns:
#             df.rename(columns={"link": "Link"}, inplace=True)
#         if "title" in df.columns:
#             df.rename(columns={"title": "Title"}, inplace=True)

#         # Only keep standard columns that exist
#         cols_to_use = [col for col in standard_columns if col in df.columns]
#         return df[cols_to_use]
#     except Exception as e:
#         print(f"Failed to load {source_name}: {e}")
#         return pd.DataFrame(columns=standard_columns)

# # Load and concatenate all datasets
# merged_df = pd.concat([load_and_standardize(path, name) for name, path in files.items()], ignore_index=True)

# # Clean the merged data
# merged_df.dropna(subset=["Title", "Link"], inplace=True)
# merged_df["Date"] = pd.to_datetime(merged_df["Date"], errors="coerce")
# merged_df = merged_df[merged_df["Date"] >= "2020-01-01"]
# merged_df.drop_duplicates(subset=["Title", "Link"], inplace=True)

# # Show basic summary
# print("📄 Merged and cleaned dataset:")
# print(merged_df.info())
# print("\n🖼️ Preview of first few rows:")
# print(merged_df.head())

# # Save to CSV for download
# merged_df.to_csv("merged_apple_news_cleaned.csv", index=False)
# print("\n✅ Saved cleaned news data to 'merged_apple_news_cleaned.csv'")