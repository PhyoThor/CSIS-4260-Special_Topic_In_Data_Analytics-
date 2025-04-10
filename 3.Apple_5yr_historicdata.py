import pandas as pd
import numpy as np
import yfinance as yf
import ta

#Download historical data for the past 5 years
df=yf.Ticker("AAPL").history(period="max")

#Add Technical Indicators

#Moving Averages
df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
df["SMA_200"] = ta.trend.sma_indicator(df["Close"], window=200)
df["EMA_50"] = ta.trend.ema_indicator(df["Close"], window=50)
df["EMA_200"] = ta.trend.ema_indicator(df["Close"], window=200)

#RSI (Relative Strength Index)
df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

#MACD (Moving Average Convergence Divergence)
df["MACD"] = ta.trend.macd(df["Close"])
df["MACD_Signal"] = ta.trend.macd_signal(df["Close"])
df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

#Bollinger Bands
df["BB_Upper"] = ta.volatility.bollinger_hband(df["Close"], window=20)
df["BB_Middle"] = ta.volatility.bollinger_mavg(df["Close"], window=20)
df["BB_Lower"] = ta.volatility.bollinger_lband(df["Close"], window=20)

#ATR (Average True Range)
df["ATR"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"], window=14)

#ADX (Average Directional Index)
df["ADX"] = ta.trend.adx(df["High"], df["Low"], df["Close"], window=14)

print(df.tail())

# **Chart 1: Apple Stock Price with Moving Averages** 
#Visualisation for better understanding

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))

# Plot Closing Price with SMA & EMA
plt.plot(df.index, df['Close'], label='Closing Price', color="blue", alpha=0.5)
plt.plot(df.index, df['SMA_50'], label='SMA 50', color="green")
plt.plot(df.index, df['SMA_200'], label='SMA 200', color="orange")
plt.plot(df.index, df['EMA_50'], label='EMA 50', color="red")
plt.plot(df.index, df['EMA_200'], label='EMA 200', color="purple")

plt.axhline(y=df['Close'].mean(), color='grey', linestyle='--', label='Mean Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Apple Stock Price with SMA & EMA')
plt.legend()
plt.show()

# **Chart 2: Apple Stock Price with Moving Average Convergence Divergence**
# Plot MACD Indicator
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['MACD'], label='MACD', color="green")
plt.plot(df.index, df['MACD_Signal'], label='Signal Line', color="red")
plt.plot(df.index, df['MACD_Hist'], label='Histogram', color="green")

plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('MACD Indicator')
plt.legend()
plt.show()
plt

# **Chart 3: Apple Stock Price with Bollinger Bands (Volatility)**
import matplotlib.patheffects as path_effects
plt.figure(figsize=(12, 8))

pe = [path_effects.Stroke(linewidth=3, foreground='black'),
      path_effects.Normal()]

plt.plot(df.index, df['Close'], label='Closing Price', color='red', linewidth=0.5)
plt.plot(df.index, df['BB_Upper'], label='Bollinger Upper Band',linestyle='dotted', color="blue")
plt.plot(df.index, df['BB_Middle'], label='Bollinger Middle Band', color="green", linestyle='dashed', alpha=0.3)
plt.plot(df.index, df['BB_Lower'], label='Bollinger Lower Band', linestyle='dotted' ,color="orange")


plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.title('Apple Stock Price with Bollinger Bands')
plt.legend()
plt.show()

# **Chart 4: RSI, ATR, and ADX** 
# 📊 Plot RSI Indicator
plt.figure(figsize=(12, 4))
plt.plot(df.index, df["RSI"], label="RSI", color="brown")
plt.axhline(70, linestyle="dashed", color="red")  # Overbought level
plt.axhline(30, linestyle="dashed", color="green")  # Oversold level
plt.title("Relative Strength Index (RSI) for Apple")
plt.legend()
plt.show()

# 📊 Plot ATR (Volatility)
plt.figure(figsize=(12, 4))
plt.plot(df.index, df["ATR"], label="ATR", color="blue")
plt.title("Average True Range (ATR) for Apple - Volatility Measure")
plt.legend()
plt.show()

# 📊 Plot ADX (Trend Strength)
plt.figure(figsize=(12, 4))
plt.plot(df.index, df["ADX"], label="ADX", color="purple")
plt.axhline(25, linestyle="dashed", color="red")  # Overbought level
plt.axhline(20, linestyle="dashed", color="green")  # Oversold level
plt.title("Average Directional Index (ADX) for Apple - Trend Strength")
plt.show()

df.to_csv("test_apple_stock_with_indicators.csv")
print("\n Apple 5-Year Stock Data with Indicators Saved as 'apple_stock_with_indicators.csv'!")