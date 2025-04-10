import requests
import pandas as pd

# Replace with your Financial Modeling Prep API key
# Yahoo Finance API was deprecated
# Alphavantage's SECTOR function does not provide individual stock listings, only sector performance.
# Hence, Financial Modeling Prep API is used to get top companies by sector.
FMP_API_KEY = "aJFp1qTffH8O0pO7beXTk8OrVlUPD6O4"

# Define the sectors of interest
sectors = {
    "Energy": "energy",
    "Technology": "technology",
    "Financials": "financial"
}
top_n = 3  # Number of top companies to extract

# Base URL for Financial Modeling Prep API
base_url = "https://financialmodelingprep.com/api/v3/stock-screener"

# Function to fetch top companies from FMP API
def get_top_companies(sector_name, sector_fmp, top_n=3):
    print(f"\n Fetching top {top_n} companies in {sector_name} sector...")

    try:
        # API Request to get companies from a sector
        params = {
            "sector": sector_fmp,
            "apikey": FMP_API_KEY,
            "limit": 20  # Fetch top 20 companies (we will sort them)
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if not data:
            print(f"⚠ No data found for {sector_name}.")
            return pd.DataFrame()

        # Convert API response to DataFrame
        df = pd.DataFrame(data)

        # Sort by Market Cap and get top N companies
        df = df.nlargest(top_n, "marketCap")[["symbol", "companyName", "marketCap"]]
        df.columns = ["Ticker", "Company", "Market Cap"]

        return df

    except Exception as e:
        print(f" Error fetching data for {sector_name}: {e}")
        return pd.DataFrame()

# Fetch top companies for each sector
results = {}
for sector_name, sector_fmp in sectors.items():
    top_companies = get_top_companies(sector_name, sector_fmp, top_n)

    if not top_companies.empty:
        results[sector_name] = top_companies

# Display results
for sector_name, top_companies in results.items():
    print(f"\n Top {top_n} Companies in {sector_name} by Market Cap:")
    print(top_companies.to_string(index=False))
    print("-" * 20)


import matplotlib.pyplot as plt
import numpy as np

# Check if there are results
if results:
    # Combine all sectors into one DataFrame
    df_all = pd.concat(results.values(), keys=results.keys()).reset_index(level=0).rename(columns={'level_0': 'Sector'})

    # Sort by Market Cap for better visualization
    df_all = df_all.sort_values("Market Cap", ascending=True)

    # Assign colors to sectors
    sector_colors = {
        "Energy": "blue",
        "Technology": "yellow",
        "Financials": "red"
    }

    # Map sector colors
    colors = df_all["Sector"].map(sector_colors)

    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(df_all["Company"], df_all["Market Cap"], color=colors, edgecolor='grey')

    # Labels & title
    plt.xlabel("Market Cap (in USD)")
    plt.ylabel("Company Name")
    plt.title(f"Top {top_n} Companies by Market Cap Across Sectors")

    # Add sector legend
    handles = [plt.Rectangle((0,0),1,1, color=sector_colors[sector]) for sector in sector_colors]
    plt.legend(handles, sector_colors.keys(), title="Sectors")

    # Show values inside bars
    for i, v in enumerate(df_all["Market Cap"]):
        plt.text(v, i, f"{v:,.0f}", ha="left", va="center", fontsize=10)

    plt.show()

else:
    print("\n⚠ No data found. Ensure your API key is correct.")