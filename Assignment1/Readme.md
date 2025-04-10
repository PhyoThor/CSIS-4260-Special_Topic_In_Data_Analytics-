# Stock Analysis & Benchmarking Project (CSIS 4260 – Assignment 1)

## Project Overview
This project focuses on **analyzing stock market data** by storing, retrieving, benchmarking, and predicting stock prices. The dataset consists of **S&P 500 stock prices from 2013 to 2018**. The project is divided into three main parts:

1. **Storing & Retrieving Data**: Comparing CSV vs. Parquet for storage and retrieval efficiency.  
2. **Analyzing & Predicting Stock Prices**: Using **Pandas vs. Polars**, implementing **technical indicators**, and applying **Machine Learning models** to predict stock prices.  
3. **Visual Dashboard**: Building **interactive dashboards** using **Streamlit & Dash** to visualize benchmarking and predictions.  

---

## Files & Their Purpose
| File Name                     | Purpose |
|--------------------------------|---------|
| `all_stocks_5yr.csv`          | Original dataset containing stock price data. |
| `Duplicating_Data.py`         | Scales dataset (1x, 10x, 100x) for benchmarking. |
| `Convert_CSVto_Parquet.py`    | Converts CSV files to Parquet for storage efficiency comparison. |
| `Benchmark_read_write.py`     | Measures read/write performance of CSV & Parquet. |
| `add_technical_indicators.py` | Adds **EMA, RSI, Bollinger Bands, and OBV** indicators to the dataset. |
| `Dataset_train.py`            | Prepares the dataset for **machine learning model training**. |
| `dashboard.py`                | **Streamlit Dashboard** for benchmarking and stock predictions. |
| `dash_dashboard.py`           | **Dash Dashboard** for visualizing benchmarking results. |
| `linear_regression_pipeline.pkl` | Trained **Linear Regression model** for stock prediction. |
| `random_forest_pipeline.pkl`  | Trained **Random Forest model** for stock prediction. |

---

## Methods & Techniques Used
### **📌 Part 1: Storing & Retrieving Data**
- **Converted CSV to Parquet** for comparison.  
- **Benchmarked read/write speeds** using Pandas & Polars.  
- **Evaluated storage efficiency** by comparing file sizes.  

### **📌 Part 2: Data Analysis & Prediction**
- **Added Technical Indicators**:
  - **EMA (Exponential Moving Average)**
  - **RSI (Relative Strength Index)**
  - **Bollinger Bands (Upper & Lower)**
  - **OBV (On-Balance Volume)**  
- **Compared Pandas vs. Polars** for performance efficiency.  
- **Implemented Machine Learning Models**:
  - **Linear Regression** (Baseline Model)
  - **Random Forest Regressor** (More complex & accurate)  
- **Performance Metrics Used**:
  - **Mean Absolute Error (MAE)**
  - **Mean Squared Error (MSE)**
  - **R² Score**
  - **Accuracy Score (%)**

### **📌 Part 3: Visualization & Dashboarding**
- **Built Streamlit Dashboard** for:
  - Benchmarking results (CSV vs. Parquet read/write speed).
  - Stock price prediction using trained ML models.
- **Developed Dash Dashboard** for benchmarking visualization.

---

## 🎯 Key Learnings
✔️ **CSV vs. Parquet**: Parquet is **more efficient** for large-scale datasets in both **storage and retrieval**.  
✔️ **Pandas vs. Polars**: **Polars is faster** than Pandas for handling large datasets.  
✔️ **Machine Learning in Finance**: Stock price prediction is **challenging**, but **Random Forest performed better** than Linear Regression.  
✔️ **Interactive Dashboards**: Streamlit and Dash provide **great visualization tools** for data analysis.  
✔️ **Benchmarking Performance**: **Parallel processing & optimized file formats significantly reduce processing time**.

---

## 📚 Libraries Used
The following Python libraries were used in this project:
pip install pandas polars scikit-learn streamlit dash plotly joblib pyarrow

Setting up the virtual environment with the comman prompt as below and how to run the rest of the steps.
  
# Step_1 (Setup Virtual Environment)
    ✔️ python -m venv venv
    ✔️ source venv/bin/activate  # On macOS/Linux
    ✔️ venv\Scripts\activate  # On Windows

# Step_2 (Install Required Libraries)
  ✔️ pip install pandas polars scikit-learn streamlit dash plotly joblib pyarrow

# Step_3 (Run Dashboards)
  ✔️ Streamlit run dashboard.py
  ✔️ python dash_dashboard.py
