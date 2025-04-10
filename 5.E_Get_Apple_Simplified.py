import pandas as pd
from openai import OpenAI
import time
import json
import csv

# === Setup OpenAI ===
client = OpenAI(api_key="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")  # Replace with your actual key

# === File Setup ===
INPUT_FILE = "apple_stock_news_with_summary_ml.csv"
OUTPUT_FILE = "apple_stock_enriched_phase2_output.csv"

# === Load & Initialize ===
df = pd.read_csv(INPUT_FILE)
#df= df.head() #------> testing purpose

# Columns to enrich
enrichment_columns = [
    "gpt_sentiment_direction", "gpt_sentiment_score",
    "gpt_positive_score", "gpt_negative_score",
    "gpt_event_type", "gpt_relevance_to_apple", "gpt_importance_score"
]

# Ensure all enrichment columns exist
for col in enrichment_columns:
    if col not in df.columns:
        df[col] = None

# #Testing
# df=df.head()

# Filter rows that need enrichment
rows_to_enrich = df[df["gpt_summary"].notna() & df[enrichment_columns].isnull().any(axis=1)].copy()
print(f"Rows to enrich: {len(rows_to_enrich)}")

# === GPT Prompt Builder ===
def build_prompt(summary):
    return f"""
You are a financial data analyst.

Given the summary of a news article below, return a JSON object with:
- sentiment_direction: One of "Positive" or "Negative" 
- sentiment_score: A float (0 to 1) showing overall tone
- positive_score: A float (0 to 1) indicating optimistic tone
- negative_score: A float (0 to 1) indicating pessimistic tone
- event_type: One of: "Product", "Financial", "Legal", "Regulatory", "Macro", or "Other"
- relevance_to_apple: Float between 0 and 1 showing how relevant it is to Apple
- importance_score: Float between 0 and 1 for article importance

Summary:
\"\"\"{summary}\"\"\"

Respond ONLY with valid JSON like:
{{
  "sentiment_direction": "Positive",
  "sentiment_score": 0.87,
  "positive_score": 0.9,
  "negative_score": 0.1,
  "event_type": "Product",
  "relevance_to_apple": 0.95,
  "importance_score": 0.88
}}

Important: If the sentiment is neutral, classify it as either "Positive" or "Negative" based on a slight leaning.
"""

# === GPT Call ===
def ask_gpt(summary, retries=2, delay=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": build_prompt(summary)}],
                temperature=0.3
            )
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("```")[-1].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error (Attempt {attempt+1}): {e}")
            time.sleep(delay)
    return None

# === Enrichment Loop ===
for count, idx in enumerate(rows_to_enrich.index, 1):
    summary = df.loc[idx, "gpt_summary"]
    print(f"[{count}/{len(rows_to_enrich)}] Enriching row {idx}...")

    result = ask_gpt(summary)
    if result:
        direction = result.get("sentiment_direction", "Positive")
        if direction not in ["Positive", "Negative"]:
            direction = "Positive"

        updates = {
            "gpt_sentiment_direction": direction,
            "gpt_sentiment_score": result.get("sentiment_score"),
            "gpt_positive_score": result.get("positive_score"),
            "gpt_negative_score": result.get("negative_score"),
            "gpt_event_type": result.get("event_type"),
            "gpt_relevance_to_apple": result.get("relevance_to_apple"),
            "gpt_importance_score": result.get("importance_score")
        }

        for col, val in updates.items():
            df.loc[idx, col] = val

        print("Enriched:", updates)
    else:
        print("Skipped due to GPT error.")

    time.sleep(0.6)

    if count % 50 == 0:
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Auto-saved at row {count}")

# === Final Save
df.to_csv(OUTPUT_FILE, index=False)
print(f"Final file saved to: {OUTPUT_FILE}")