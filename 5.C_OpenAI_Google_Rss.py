from openai import OpenAI
import pandas as pd
import json
import re
import time

# === CONFIGURATION ===
client = OpenAI(api_key="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")  # Replace with your key
input_file = "./.venv/data/apple_google_news_rss.csv"  # or full dataset path
output_file = "./.venv/data/apple_google_news_enriched.csv"

# === LOAD DATA ===
df = pd.read_csv(input_file)
df = df[df["gpt_summary"].notna()].copy()
df.reset_index(drop=True, inplace=True)

# === GPT ENRICHMENT FUNCTION ===
def analyze_text(title, summary):
    prompt = f"""
You are an analyst. Based on this Apple-related news, return:
1. Sentiment label (Positive / Neutral / Negative)
2. Sentiment score (scale 1–10)
3. Short sentiment reasoning
4. Topic label (e.g., Finance, Product, Legal, Market)
5. Event type (e.g., Launch, Lawsuit, Earnings, Acquisition)
6. Relevance to Apple (True or False)

Headline: {title}
Summary: {summary}

Respond in this JSON format:
{{
  "sentiment_label": "...",
  "sentiment_score": ...,
  "sentiment_reason": "...",
  "topic_label": "...",
  "event_type": "...",
  "relevance_to_apple": true
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial news analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        raw = response.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            return pd.Series([
                data.get("sentiment_label", "NA"),
                data.get("sentiment_score", "NA"),
                data.get("sentiment_reason", "NA"),
                data.get("topic_label", "NA"),
                data.get("event_type", "NA"),
                data.get("relevance_to_apple", "NA")
            ])
        else:
            return pd.Series(["ERROR"] * 6)
    except Exception as e:
        print(f"Error: {e}")
        return pd.Series(["ERROR"] * 6)

# === PROCESS FULL DATASET WITH DELAY ===
results = []
for i, row in df.iterrows():
    print(f"🔄 Processing row {i+1}/{len(df)}: {row['Title'][:60]}...")
    enriched = analyze_text(row["Title"], row["gpt_summary"])
    results.append(enriched)
    time.sleep(3)  # Safety delay to avoid rate limits

# === SAVE OUTPUT ===
columns = [
    "gpt_sentiment_label",
    "gpt_sentiment_score",
    "gpt_sentiment_reason",
    "gpt_topic_label",
    "gpt_event_type",
    "gpt_relevance_to_apple"
]
df[columns] = pd.DataFrame(results, index=df.index)
df.to_csv(output_file, index=False)

print(f"\n✅ Enrichment complete! Saved to: {output_file}")
