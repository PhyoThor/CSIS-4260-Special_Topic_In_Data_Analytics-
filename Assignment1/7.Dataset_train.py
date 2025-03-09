import polars as pl
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# ---- Load Dataset ----
df = pl.read_csv("all_stocks_5yr_with_indicators.csv")

# Drop rows with NaN (if any)
df = df.drop_nulls()

# Select features (X) and target variable (y)
features = ["EMA_50", "RSI", "BB_upper", "BB_lower", "OBV"]
X = df.select(features).to_numpy()  # Convert to NumPy
df = df.with_columns(df["close"].shift(-1).alias("target"))
y = df["target"].to_numpy()

# Drop last row (since it doesn't have a "next day" value)
X = X[:-1]
y = y[:-1]

# Split into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---- Create ML Pipelines ----
lr_pipeline = Pipeline([
    ("scaler", StandardScaler()),  
    ("lr", LinearRegression())     
])

rf_pipeline = Pipeline([
    ("scaler", StandardScaler()),  
    ("rf", RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=42))  
])

lr_pipeline.fit(X_train, y_train)
rf_pipeline.fit(X_train, y_train)

# ---- Make Predictions ----
lr_pred = lr_pipeline.predict(X_test)
rf_pred = rf_pipeline.predict(X_test)

# ---- Accuracy Score Calculation ----
def calculate_accuracy(y_true, y_pred):
    # """Calculate accuracy for regression as (100% - Mean Absolute Percentage Error)."""
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return 100 - mape  # The Higher is the better


def evaluate_model(model_name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    accuracy = calculate_accuracy(y_true, y_pred)

    print(f"\n{model_name} Performance:")
    print(f"   - Mean Absolute Error (MAE): {mae:.4f}")
    print(f"   - Mean Squared Error (MSE): {mse:.4f}")
    print(f"   - R² Score: {r2:.4f} (Higher is better)")
    print(f"   - Accuracy Score: {accuracy:.2f}%")

# ---- Print Final Results (Only Once) ----
evaluate_model("Linear Regression", y_test, lr_pred)
evaluate_model("Random Forest", y_test, rf_pred)

# ---- Save the trained models (Uncomment if needed) ----
# joblib.dump(lr_pipeline, "linear_regression_pipeline.pkl")
# joblib.dump(rf_pipeline, "random_forest_pipeline.pkl")

# print("\nPipelines saved successfully!")
