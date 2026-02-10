# Apple Stock Prediction Project

## Overview
This project analyzes and predicts Apple Inc. (AAPL) stock price movements by combining historical stock data with news sentiment analysis. The system integrates technical indicators, news article sentiment scores, and machine learning models to forecast stock price trends.

## Project Objectives
- Collect and analyze Apple stock historical data with technical indicators
- Gather and process news articles from multiple sources related to Apple
- Perform sentiment analysis and topic modeling on news data
- Merge stock and news data for comprehensive analysis
- Build machine learning models to predict stock price movements
- Create an interactive dashboard for visualization and analysis

## Data Sources

### Stock Data
- **Source**: Yahoo Finance (yfinance API)
- **Period**: 5 years of historical data
- **Features**: Open, High, Low, Close, Volume, Dividends, Stock Splits

### News Data
The project aggregates news from multiple sources:
- **NewsAPI**: News articles via API rotation
- **Yahoo Finance News**: Apple-related news from Yahoo Finance
- **Google RSS Feed**: Google News RSS feed for Apple
- **RSS Queries**: Custom RSS queries for Apple news

## Technical Indicators
The following technical indicators are calculated for stock analysis:

- **Moving Averages**: SMA (50, 200), EMA (50, 200)
- **RSI (Relative Strength Index)**: Momentum indicator (14-day window)
- **MACD (Moving Average Convergence Divergence)**: Trend-following indicator
- **Bollinger Bands**: Volatility indicator (20-day window)
- **ATR (Average True Range)**: Volatility measure
- **ADX (Average Directional Index)**: Trend strength indicator

## Data Processing Pipeline

### 1. Industry Analysis (`1.industry_analysis.py`)
- Analyzes top industries with highest 5-year returns
- Identifies top companies by sector

### 2. Stock Data Collection (`3.Apple_5yr_historicdata.py`)
- Downloads historical Apple stock data
- Calculates technical indicators
- Generates visualization charts

### 3. News Collection (Scripts 4.A-4.D)
- `4.A_AppleNews_Queries_RSS.py`: RSS query-based news collection
- `4.B_AppleNews_Scrape_NewsAPI.py`: NewsAPI scraping
- `4.C_AppleNews_Scrape_Yfinance.py`: Yahoo Finance news extraction
- `4.D_AppleNews_GoogleRSS.py`: Google RSS feed processing

### 4. Data Preprocessing (Scripts 5.A-5.E)
- `5.A_Preprocessing.py`: Text cleaning and preprocessing
- `5.B_Topic_Modeling_BERTopic.py`: Topic modeling using BERTopic
- `5.C_Generate_Summary.py`: Generate article summaries
- `5.D_News_MergeNClean_extracted_files.py`: Merge and clean news data
- `5.E_Get_Apple_Simplified.py`: Simplify Apple dataset

### 5. Feature Engineering (Scripts 6.A-6.D)
- `6.A_Overview Summary.py`: Generate overview summaries
- `6.B_Keywords_Evaluation.py`: Extract and evaluate keywords
- `6.C_Drop_in_Audit.py`: Data quality auditing
- `6.D_Audit_part2.py`: Additional data validation

### 6. Data Integration
- `7.Clean_Date_Format.py`: Standardize date formats
- `8.A_Correlation_Analysis.py`: Analyze correlations between features
- `9.A_Merge_news_and_data.py`: Merge news sentiment with stock data

## Machine Learning Models

The project implements three regression models for stock price prediction:

### 1. Random Forest Regressor
- Ensemble learning method
- 100 estimators
- StandardScaler preprocessing

### 2. XGBoost Regressor
- Gradient boosting algorithm
- 50 estimators
- Learning rate: 0.2
- Max depth: 10

### 3. Polynomial Regression
- Degree 3 polynomial features
- Linear regression on polynomial features

### Features Used
- Volume
- MACD and MACD_Hist
- ATR (Average True Range)
- ADX (Average Directional Index)
- GPT Sentiment Score
- GPT Positive/Negative Scores
- GPT Relevance to Apple
- GPT Importance Score
- RSI (Relative Strength Index)

### Target Variable
Log returns: `log(Close[t+1]) - log(Close[t])`

### Evaluation Metrics
- R² Score
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

## Interactive Dashboard

The project includes a Streamlit dashboard (`APPLE_Dashboard.py`) that provides:
- Model performance comparison
- Feature importance visualization
- Historical stock price charts with technical indicators
- Sentiment score analysis
- Interactive predictions

### Running the Dashboard
```bash
streamlit run APPLE_Dashboard.py
```

## Project Structure
```
.
├── 1.industry_analysis.py                    # Industry analysis
├── 2.top_3_companiesofsectors.py            # Top companies by sector
├── 3.Apple_5yr_historicdata.py              # Historical stock data collection
├── 4.A-4.D_AppleNews_*.py                   # News collection scripts
├── 5.A-5.E_*.py                             # Data preprocessing pipeline
├── 6.A-6.D_*.py                             # Feature engineering
├── 7.Clean_Date_Format.py                   # Date formatting
├── 8.A_Correlation_Analysis.py              # Correlation analysis
├── 9.A_Merge_news_and_data.py              # Data merging
├── save models.py                           # Model training and saving
├── APPLE_Dashboard.py                       # Streamlit dashboard
├── requirements.txt                         # Python dependencies
└── README.md                                # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/PhyoThor/CSIS-4260-Special_Topic_In_Data_Analytics-.git
cd CSIS-4260-Special_Topic_In_Data_Analytics-
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Additional required packages:
```bash
pip install yfinance ta bertopic sentence-transformers xgboost openai
```

## Usage

### 1. Collect Stock Data
```bash
python 3.Apple_5yr_historicdata.py
```

### 2. Collect News Data
Run news collection scripts in sequence:
```bash
python 4.A_AppleNews_Queries_RSS.py
python 4.B_AppleNews_Scrape_NewsAPI.py
python 4.C_AppleNews_Scrape_Yfinance.py
python 4.D_AppleNews_GoogleRSS.py
```

### 3. Process and Merge Data
```bash
python 5.A_Preprocessing.py
python 9.A_Merge_news_and_data.py
```

### 4. Train Models
```bash
python "save models.py"
```

### 5. Launch Dashboard
```bash
streamlit run APPLE_Dashboard.py
```

## Key Features

- **Multi-source News Aggregation**: Combines news from NewsAPI, Yahoo Finance, and Google RSS
- **Advanced NLP**: Uses BERTopic for topic modeling and GPT for sentiment analysis
- **Technical Analysis**: Comprehensive technical indicators (RSI, MACD, Bollinger Bands, etc.)
- **Machine Learning**: Multiple regression models with ensemble methods
- **Interactive Visualization**: Streamlit dashboard for real-time analysis
- **Correlation Analysis**: Examines relationships between news sentiment and stock movements

## Visualizations

The project generates various visualizations including:
- Stock price charts with moving averages
- Technical indicator overlays (RSI, MACD, Bollinger Bands, ATR, ADX)
- Sentiment score distributions
- Topic trends over time
- Correlation heatmaps
- Model performance comparisons

## Data Files

Key output files include:
- `apple_stock_enriched_phase2_output.csv`: Final merged dataset with all features
- `apple_news_stock_enriched.csv`: News-stock merged dataset
- `apple_stock_with_indicators.csv`: Stock data with technical indicators
- Model predictions: `y_pred_rf.npy`, `y_pred_xgb.npy`, `y_pred_poly.npy`
- Model metrics: `metrics_rf.npy`, `metrics_xgb.npy`, `metrics_poly.npy`

## Technologies Used

- **Python 3.x**
- **Data Collection**: yfinance, NewsAPI, RSS feeds
- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn, XGBoost
- **NLP**: BERTopic, sentence-transformers, OpenAI GPT
- **Technical Analysis**: ta (Technical Analysis Library)
- **Visualization**: matplotlib, seaborn, Streamlit
- **Web Scraping**: BeautifulSoup (implied)

## Course Information
**Course**: CSIS 4260 - Special Topic in Data Analytics  
**Institution**: [Your Institution Name]  
**Project Type**: Stock Market Prediction using Machine Learning and Sentiment Analysis

## License
This project is part of an academic assignment for CSIS 4260.

## Contributors
PhyoThor

## Notes
- Ensure you have valid API keys for NewsAPI and OpenAI GPT if using those features
- Stock market predictions are for educational purposes only
- Past performance does not guarantee future results