import pandas as pd
import ta

# Function to add top 4 market-used technical indicators
def add_indicators(df):
    print("\n Adding Market's Top 4 Technical Indicators for stock price prediction...")

    # 1️ Exponential Moving Average (EMA 50)
    df["EMA_50"] = ta.trend.ema_indicator(df["close"], window=50)

    # 2️ Relative Strength Index (RSI)
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)

    # 3️ Bollinger Bands (Upper bound & Lower bound)
    df["BB_upper"] = ta.volatility.bollinger_hband(df["close"], window=20)
    df["BB_lower"] = ta.volatility.bollinger_lband(df["close"], window=20)

    # 4️ On-Balance Volume (OBV)
    df["OBV"] = ta.volume.on_balance_volume(df["close"], df["volume"])

    print(" Technical Indicators Added Successfully!")
    return df

if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv("all_stocks_5yr.csv")

    # Add the indicators
    df = add_indicators(df)

    # Save the enhanced dataset
    df.to_csv("all_stocks_5yr_with_indicators.csv", index=False)
    print(" Enhanced dataset saved as 'all_stocks_5yr_with_indicators.csv'")
