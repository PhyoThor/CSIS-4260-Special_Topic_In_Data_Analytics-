# 📊 Apple Stock Price Movement Prediction
## 🚀 Live Dashboard

You can explore the interactive stock prediction dashboard here:

👉 [View Streamlit App](https://csis-4260-specialtopicindataanalytics-git-rgmtpshqpazxqz8ofacx.streamlit.app/)

## 🧠 Project Overview

This project aims to predict the next-day movement of Apple Inc.'s stock price using a hybrid dataset composed of technical indicators and GPT-enriched financial news features. The goal is to simulate real-world analyst behavior by blending quantitative price data with qualitative sentiment signals, allowing for more holistic and explainable stock movement predictions.

## 🍏 Why Apple?

Apple Inc. was selected as the focal company for several reasons:
- **High market capitalization** and global investor interest.
- **Consistent media coverage**, providing a large pool of text data.
- **Tech-sector relevance**, aligning with volatile and trend-driven price patterns.
- **Previous inclusion in benchmark indexes** like the S&P 500 and NASDAQ.

These factors ensure both data richness and practical value for modeling purposes.

## 🗃️ Data Collection

1. **Stock Price Data**  
   Source: [Yahoo Finance](https://finance.yahoo.com)  
   - Collected using `yfinance` Python package.
   - Historical daily stock data (Open, High, Low, Close, Volume) retrieved from 2010 to 2024.

2. **Financial News Data**  
   Sources: Google News RSS, NewsAPI, and Yahoo Finance News  
   - Scraped using libraries like `requests`, `BeautifulSoup`, and `PRAW`.
   - Filtered for Apple-related headlines between 2020 and 2024.
   - Enriched using OpenAI’s GPT API to extract:
     - Sentiment direction & score
     - Relevance to Apple
     - Importance score
     - Positive/Negative breakdown
     - Event classification

## 📈 Feature Engineering

- **Technical Indicators**:  
  - RSI, MACD, MACD Histogram, ADX, ATR, Bollinger Bands, SMA, EMA, etc.
  - Engineered using `ta-lib` and `pandas_ta`.

- **GPT-Enriched Features**:  
  - `gpt_sentiment_score`, `gpt_importance_score`, `gpt_relevance_to_apple`, etc.

- **Target Variable**:  
  - Defined as the **log-return** of the next day’s closing price:
    ```python
    df["target"] = np.log(df["Close"].shift(-1)) - np.log(df["Close"])
    ```

## 🤖 Machine Learning Models

The following algorithms were trained and evaluated:
- Random Forest Regressor
- XGBoost Regressor
- Gradient Boosting Regressor
- Ridge Regression
- Polynomial Regression (Degree 3)
- LSTM Neural Network *(later removed for dashboard simplicity)*

Each model's performance was compared using:
- R² Score
- MAE, RMSE
- Binary Accuracy (based on direction: Up/Down)

## 📊 Dashboard with Streamlit

A Streamlit-powered interactive dashboard was built to:
- View model predictions
- Compare actual vs predicted values
- Visualize scatter plots and metrics

## 🛠️ Required Libraries

pip install -r requirements.txt

git clone https://github.com/your-username/apple-stock-prediction.git
cd apple-stock-prediction
Activate virtual environment:

python -m venv .venv
.venv\Scripts\activate
Install dependencies:

Run the dashboard:
streamlit run dashboard.py
