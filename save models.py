import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb

# --- Load Data ---
df = pd.read_csv("apple_stock_enriched_phase2_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)
df["target"] = np.log(df["Close"].shift(-1)) - np.log(df["Close"])
df = df.dropna(subset=["target"]).reset_index(drop=True)

features = ['Volume','MACD', 'MACD_Hist', 'ATR', 'ADX', 
            'gpt_sentiment_score', 'gpt_positive_score',
            'gpt_negative_score', 'gpt_relevance_to_apple',
            'gpt_importance_score']

X = df[features]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Train Random Forest ---
rf_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])
rf_pipeline.fit(X_train, y_train)
y_pred_RF = rf_pipeline.predict(X_test)

# --- Train XGBoost ---
xgb_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('xgb', xgb.XGBRegressor(
        n_estimators=50,
        learning_rate=0.2,
        max_depth=10,
        random_state=42,
        objective='reg:squarederror'
    ))
])
xgb_pipeline.fit(X_train, y_train)
y_pred_XGB = xgb_pipeline.predict(X_test)

# --- Train Polynomial Regression ---
poly_model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
poly_model.fit(X_train, y_train)
y_pred_poly = poly_model.predict(X_test)

# --- Evaluation Function ---
def get_metrics(y_true, y_pred):
    return {
        "r2": r2_score(y_true, y_pred),
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred))
    }

metrics_rf = get_metrics(y_test, y_pred_RF)
metrics_xgb = get_metrics(y_test, y_pred_XGB)
metrics_poly = get_metrics(y_test, y_pred_poly)

# --- Save Predictions ---
np.save("y_pred_rf.npy", y_pred_RF)
np.save("y_pred_xgb.npy", y_pred_XGB)
np.save("y_pred_poly.npy", y_pred_poly)

# --- Save Metrics ---
np.save("metrics_rf.npy", metrics_rf)
np.save("metrics_xgb.npy", metrics_xgb)
np.save("metrics_poly.npy", metrics_poly)

print("✅ All model outputs saved as .npy files.")
