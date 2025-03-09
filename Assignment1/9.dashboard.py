import streamlit as st
import polars as pl
import plotly.express as px
import joblib  # For loading trained ML models
import pandas as pd  # Needed for ML model compatibility

# ---- Load Benchmark Results ----
@st.cache_data
def load_benchmark_results():
    df = pd.read_csv("benchmark_results.csv")

    # Ensure correct column names
    if "Time (Seconds)" in df.columns:
        df.rename(columns={"Time (Seconds)": "Execution Time"}, inplace=True)
    elif "Read Time" in df.columns:
        df.rename(columns={"Read Time": "Execution Time"}, inplace=True)

    return df

# ---- Load Stock Data ----
@st.cache_data
def load_stock_data():
    df = pl.read_csv("all_stocks_5yr_with_indicators.csv")  # Using CSV for compatibility
    df = df.fill_null(strategy="forward")  # Handle missing values
    return df

# ---- Load ML Models ----
@st.cache_resource
def load_models():
    lr_model = joblib.load("linear_regression_pipeline.pkl")
    rf_model = joblib.load("random_forest_pipeline.pkl")
    return lr_model, rf_model

# ---- Predict Stock Prices ----
def predict_price(model, stock_data):
    features = ["EMA_50", "RSI", "BB_upper", "BB_lower", "OBV"]
    stock_data = stock_data.select(features).to_pandas()
    return model.predict(stock_data)

# ---- Sidebar Navigation ----
st.sidebar.title(" Stock Analysis Dashboard")
page = st.sidebar.radio("Select a section:", ["Benchmarking Results", "Stock Price Prediction"])

# ---- Benchmarking Results Visualization ----
if page == "Benchmarking Results":
    st.markdown("<h1 style='text-align: center;'> Benchmarking Performance Comparison and Stock Prediction Dashboard</h1>", unsafe_allow_html=True)

    benchmark_data = load_benchmark_results()

    # Read Speed Comparison Chart with Data Labels
    fig = px.bar(
        benchmark_data[benchmark_data["Operation"] == "Read"],
        x="Dataset", y="Execution Time", color="Library",
        barmode="group",
        text_auto=".2f",  # Display values inside bars
        title="CSV vs. Parquet Read Speed Comparison"
    )
    st.plotly_chart(fig)

    #  Write Speed Comparison Chart with Data Labels
    fig2 = px.bar(
        benchmark_data[benchmark_data["Operation"] == "Write"],
        x="Dataset", y="Execution Time", color="Library",
        barmode="group",
        text_auto=".2f",  # Display values inside bars
        title="CSV vs. Parquet Write Speed Comparison",
        color_discrete_sequence=["#FFA15A", "#7F8486"]
    )
    st.plotly_chart(fig2)

elif page == "Stock Price Prediction":
    st.title(" Stock Price Prediction")

    stock_data = load_stock_data()

    #  Ensure Ticker Consistency
    stock_data = stock_data.with_columns(pl.col("name").str.strip_chars())  
    stock_tickers = stock_data["name"].unique().to_list()
    stock_tickers = [str(ticker) for ticker in stock_tickers]

    #  Sort Stock Tickers in Ascending Order
    stock_tickers.sort()
    selected_ticker = st.selectbox("Choose a stock ticker:", stock_tickers)
    selected_ticker = str(selected_ticker)  

    #  Filter Data Correctly
    stock_filtered = stock_data.filter(pl.col("name").cast(pl.Utf8) == selected_ticker)

    if stock_filtered.shape[0] == 0:
        st.error(f"No data available for {selected_ticker}. Please select another stock.")
        st.stop()

    #  Load Models
    lr_model, rf_model = load_models()

    #  Generate Predictions
    stock_filtered = stock_filtered.with_columns([
        pl.Series("LR_Predicted", predict_price(lr_model, stock_filtered)),
        pl.Series("RF_Predicted", predict_price(rf_model, stock_filtered))
    ])

    #  Plot Actual vs Predicted Prices
    fig3 = px.line(
        stock_filtered.to_pandas(),
        x="date", y=["close", "LR_Predicted", "RF_Predicted"],
        labels={"value": "Stock Price", "date": "Date"},
        title=f"Predicted vs. Actual Prices for {selected_ticker}"
    )
    st.plotly_chart(fig3)

    # Show Predictions in Table
    st.write(" Model Predictions:")
    st.dataframe(stock_filtered[["date", "close", "LR_Predicted", "RF_Predicted"]].to_pandas())
