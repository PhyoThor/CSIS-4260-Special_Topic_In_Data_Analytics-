# **Evaluation of the cleaned dataset**

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned merged file
df = pd.read_csv(".venv/data/merged_apple_news_cleaned_full.csv", parse_dates=["Date"])
df['Date'] = pd.to_datetime(df['Date'],errors="coerce")
plt.style.use("ggplot")

# === BASIC OVERVIEW ===
print(" Dataset Info:")
print(df.info(), "\n")

print(" Article Count by Source:")
print(df["Source"].value_counts(), "\n")

print(" Date Range:")
print(f"From {df['Date'].min().date()} to {df['Date'].max().date()}\n")

print(" Null Value Count:")
print(df.isnull().sum(), "\n")

# Add Title Length column
df["Title Length"] = df["Title"].str.len()
print(" Title Length Stats:")
print(df["Title Length"].describe(), "\n")

# Overview Summary
overview = {
    "Total Articles": len(df),
    "Date Range": f"{df['Date'].min().date()} to {df['Date'].max().date()}",
    "Sources": df['Source'].value_counts().to_dict(),
    "Missing Values": df.isnull().sum().to_dict(),
    "Duplicates Removed": df.duplicated(subset=["Title", "Date"]).sum()
}

print("\n🔍 Overview Summary:")
for key, value in overview.items():
    print(f"{key}: {value}")

# === PLOT: Monthly Article Frequency ===
df_by_month = df.set_index("Date").resample("ME").size()

plt.figure(figsize=(10, 5))
df_by_month.plot(marker='o')
plt.title("Article Frequency Over Time (Monthly)")
plt.xlabel("Month")
plt.ylabel("Number of Articles")
plt.tight_layout()
plt.grid(True)
plt.show()


