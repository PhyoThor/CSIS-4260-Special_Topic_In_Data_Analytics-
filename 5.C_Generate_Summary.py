import pandas as pd
from openai import OpenAI
import time
import json

# === GPT Setup ===
client = OpenAI(api_key="xx")  # Replace with your API key

# === File Paths ===
INPUT_FILE = "apple_stock_news_clean_start.csv"
OUTPUT_FILE = "apple_stock_news_with_summary_ml.csv"

# === Load Data ===
df = pd.read_csv(INPUT_FILE)


# === Add gpt_summary column if missing ===
if "gpt_summary" not in df.columns:
    df["gpt_summary"] = None
    #df=df.head(3) >>>>>>>>> for testing only


# === Filter only rows with missing summary
df_to_enrich = df[df["gpt_summary"].isna()].copy()
print(f" Resuming enrichment: {len(df_to_enrich)} rows left")

# === Define prompt builder ===
def build_summary_prompt(text):
    return f"""
Summarize the following financial news article in 1-2 sentences from an investor's perspective:

\"\"\"{text}\"\"\"
"""

# === GPT call ===
def generate_summary(text, retries=3, delay=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": build_summary_prompt(text)}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f" Error on attempt {attempt+1}: {e}")
            time.sleep(delay)
    return None

# === Loop through rows ===
for i, idx in enumerate(df_to_enrich.index):
    title = df.loc[idx, "Title"]  # Safe: your real title column
    print(f" {i+1}: Enriching row {idx} - {title}")
    summary = generate_summary(title)
    if summary:
        df.at[idx, "gpt_summary"] = summary
        print(" Summary:", summary)
    else:
        print(" Skipped due to error")

    time.sleep(0.6)

    # Auto-save every 50 rows
    if i % 50 == 0:
        df.to_csv("apple_stock_news_with_summary_ml.csv", index=False)
        print(f" Auto-saved at row {i+1}")

# === Save to file ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n Saved file with GPT summaries to:\n→ {OUTPUT_FILE}")
