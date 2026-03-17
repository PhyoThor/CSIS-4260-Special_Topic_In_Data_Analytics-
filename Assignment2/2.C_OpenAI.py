import pandas as pd
from openai import OpenAI
import time
import json

client = OpenAI(api_key="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")

# ------------------- Prompt Template -------------------
prompt_template = """
You are an expert financial analyst. Given the following post or article text:

\"\"\"{text}\"\"\"

1. Provide a short summary (1-2 sentences).
2. Give it an importance score from -1 (very negative) to +1 (very positive), considering its impact on NVIDIA stock or public sentiment.

Respond in this JSON format:
{{ 
  "summary": "...", 
  "score": 0.0 
}}
"""

# ------------------- GPT Enrichment Function -------------------
def gpt_enrich(text):
    if not isinstance(text, str) or text.strip() == "":
        return {"summary": "", "score": 0.0}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize and score financial text."},
                {"role": "user", "content": prompt_template.format(text=text)}
            ],
            temperature=0.2,
            max_tokens=200
        )
        content = response.choices[0].message.content.strip()
        print("\n GPT raw content:\n", content)

        # If wrapped in markdown, strip it
        if content.startswith("```"):
            content = content.split("```")[-1].strip()

        result = json.loads(content)
        return result

    except json.JSONDecodeError as je:
        print(" JSON parsing failed:", je)
        return {"summary": "", "score": 0.0}

    except Exception as e:
        print(f" OpenAI API Exception: {e}")
        return {"summary": "", "score": 0.0}

# ------------------- Score to Direction -------------------
def score_to_direction(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    return "Neutral"

# ------------------- Enrichment Pipeline -------------------
def openai_pipeline(input_file, output_file, source):
    print(f"\n Enriching {source} with OpenAI GPT...")

    df = pd.read_csv(input_file)  # 👈 TEMP: First 3 rows only for testing

    summaries = []
    scores = []

    for i, row in df.iterrows():
        text = row.get("clean_text", "")
        enriched = gpt_enrich(text)
        summaries.append(enriched["summary"])
        scores.append(enriched["score"])
        time.sleep(2.5)  # Rate limit protection

    df["gpt_summary"] = summaries
    df["gpt_score"] = scores
    df["gpt_direction"] = df["gpt_score"].apply(score_to_direction)

    df.to_csv(output_file, index=False)
    print(f" Saved enriched file to: {output_file}")

# ------------------- Run for Reddit + CNN -------------------
if __name__ == "__main__":
    openai_pipeline("nvidia_praw_keywords.csv", "nvidia_praw_enriched.csv", source="Reddit")
    openai_pipeline("nvidia_cnn_bing_keywords.csv", "nvidia_cnn_bing_enriched.csv", source="CNN")
