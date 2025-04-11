# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# --- Load and preprocess data ---
@st.cache_data
def load_data():
    df = pd.read_csv("apple_stock_enriched_phase2_output.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["target"] = np.log(df["Close"].shift(-1)) - np.log(df["Close"])
    df = df.dropna(subset=["target"]).reset_index(drop=True)
    features = ['Volume','MACD', 'MACD_Hist', 'ATR', 'ADX', 
                'gpt_sentiment_score', 'gpt_positive_score',
                'gpt_negative_score', 'gpt_relevance_to_apple',
                'gpt_importance_score', 'RSI']
    return df, features

df, features = load_data()
X = df[features]
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Train models ---
@st.cache_data
def train_models(X_train, y_train):
    models = {}

    rf_model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    rf_model.fit(X_train, y_train)
    models["Random Forest"] = rf_model

    ridge_model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', Ridge(alpha=10))
    ])
    ridge_model.fit(X_train, y_train)
    models["Ridge Regression"] = ridge_model

    gbr_model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42))
    ])
    gbr_model.fit(X_train, y_train)
    models["Gradient Boosting"] = gbr_model

    return models

models = train_models(X_train, y_train)

# --- Streamlit UI ---
st.title("\U0001F4C8 Apple Stock Price Prediction Dashboard")
model_choice = st.selectbox("Choose a model to evaluate:", list(models.keys()))
model = models[model_choice]

# --- Predict and Evaluate ---
y_pred = model.predict(X_test)
threshold = 0  # log-return threshold
y_test_bin = (y_test > threshold).astype(int)
y_pred_bin = (y_pred > threshold).astype(int)

# --- Show Actual vs Predicted Table ---
st.subheader("\U0001F4CB Actual vs Predicted Table")
col1, col2, col3, col4 = st.columns(4)
col1.metric("R² Score", f"{r2_score(y_test, y_pred):.4f}")
col2.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.4f}")
col3.metric("MSE", f"{mean_squared_error(y_test, y_pred):.4f}")
col4.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# --- Model Comparison ---
st.subheader("📊 Model Performance Comparison")
scores_df = pd.DataFrame(columns=["Model", "R2", "MAE", "RMSE"])
for name, mdl in models.items():
    y_pred_all = mdl.predict(X_test)
    scores_df = pd.concat([scores_df, pd.DataFrame({
        "Model": [name],
        "R2": [r2_score(y_test, y_pred_all)],
        "MAE": [mean_absolute_error(y_test, y_pred_all)],
        "RMSE": [np.sqrt(mean_squared_error(y_test, y_pred_all))]
    })])

fig, ax = plt.subplots(figsize=(10, 4))
sb.barplot(data=scores_df.melt(id_vars='Model'), x='Model', y='value', hue='variable', ax=ax)
ax.set_title("Model Comparison: R², MAE, RMSE")
st.pyplot(fig)


# Convert to DataFrame
comparison_df = pd.DataFrame({
    "Date": df.loc[y_test.index, "Date"].values[:len(y_pred)],
    "Actual Change": y_test.values[:len(y_pred)],
    "Predicted Change": y_pred,
    "Actual Close": df.loc[y_test.index, "Close"].values[:len(y_pred)]
})

# Add Close Price + Prediction
comparison_df["Predicted Close"] = comparison_df["Actual Close"] * np.exp(comparison_df["Predicted Change"])

# Add Up/Down arrow column
comparison_df["\U0001F4C8 Direction"] = comparison_df["Predicted Change"].apply(lambda x: "⬆️" if x > 0 else "⬇️")

# Round for display
comparison_df["Actual Change"] = comparison_df["Actual Change"].round(2)
comparison_df["Predicted Change"] = comparison_df["Predicted Change"].round(2)
comparison_df["Predicted Close"] = comparison_df["Predicted Close"].round(2)
comparison_df["Actual Close"] = comparison_df["Actual Close"].round(2)

# Show table
num_rows = st.slider("Rows to display", 5, 100, 20)
st.dataframe(
    comparison_df[["Date", "Actual Change", "Predicted Change", "Actual Close", "Predicted Close", "\U0001F4C8 Direction"]].head(num_rows),
    use_container_width=True
)

st.subheader("📉 Actual vs Predicted Close Price")
line_chart_df = comparison_df.set_index("Date")[["Actual Close", "Predicted Close"]]
st.line_chart(line_chart_df)

st.markdown("### Explanation of the table columns:")
st.markdown("""
- **Date**: The date of the stock price.
- **Close**: The actual closing price of Apple stock on that date.
- **Predicted_Close**: The predicted closing price based on the model.
- **Actual_Close**: The actual closing price based on the log-return.
- **Predicted_LogReturn**: The predicted log-return of the stock price.
- **Actual_LogReturn**: The actual log-return of the stock price.
""")

st.markdown("### Note:")
st.markdown("""
The predicted and actual closing prices are calculated using the formula:
`Predicted_Close = Close * exp(Predicted_LogReturn)`
`Actual_Close = Close * exp(Actual_LogReturn)`
""")

st.markdown("### Additional Information:")
st.markdown("""
- The log-return is calculated as:
`log-return = log(Close_today / Close_yesterday)`
- The log-return is used to predict the future price of the stock.
- The predicted log-return is the output of the model.
- The actual log-return is calculated based on the actual closing prices.
""")

st.markdown("### Model Evaluation Metrics:")
st.markdown(f"""
- **R^2 Score**: {r2_score(y_test, y_pred):.4f}
- **Mean Absolute Error**: {mean_absolute_error(y_test, y_pred):.4f}
- **Mean Squared Error**: {mean_squared_error(y_test, y_pred):.4f}
- **Root Mean Squared Error**: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}
""")

st.markdown("### Confusion Matrix:")
conf_matrix = confusion_matrix(y_test_bin, y_pred_bin)
fig, ax = plt.subplots()
sb.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
ax.set_title("Confusion Matrix")
st.pyplot(fig)

st.markdown("### Feature Importance:")
importances = model.named_steps['model'].feature_importances_
feature_importances = pd.DataFrame(importances, index=X.columns, columns=["Importance"]).sort_values("Importance", ascending=False)
st.bar_chart(feature_importances)
st.markdown("### Feature Importance Table:")
st.dataframe(feature_importances)
st.markdown("### Explanation of Feature Importance:")
st.markdown("""
- **Feature Importance**: Indicates how much each feature contributes to the model's predictions.
- **Higher values** indicate that the feature is more important for the model.
- **Lower values** indicate that the feature is less important for the model.
""")
st.markdown("### Note:")
st.markdown("""
- The feature importance values are calculated based on the trained model.
- The values are normalized to sum to 1.
- The feature importance values can be used to understand which features are most important for the model's predictions.
""")

st.markdown("### Permutation Feature Importance:")
from sklearn.inspection import permutation_importance
perm_importance = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
perm_importance_df = pd.DataFrame(perm_importance.importances_mean, index=X.columns, columns=["Importance"]).sort_values("Importance", ascending=True)
st.bar_chart(perm_importance_df)
st.markdown("### Permutation Feature Importance Table:")
st.dataframe(perm_importance_df)
st.markdown("### Explanation of Permutation Feature Importance:")
st.markdown("""
- **Permutation Feature Importance**: Measures the change in model performance when the values of a feature are randomly shuffled.
- **Higher values** indicate that the feature is more important for the model.
- **Lower values** indicate that the feature is less important for the model.
""")
st.markdown("### Note:")
st.markdown("""
- The permutation feature importance values are calculated based on the trained model.
- The values are normalized to sum to 1.
- The permutation feature importance values can be used to understand which features are most important for the model's predictions.
""")
st.markdown("### Additional Information:")
st.markdown("""
- The permutation feature importance values are calculated based on the trained model.
- The values are normalized to sum to 1.
- The permutation feature importance values can be used to understand which features are most important for the model's predictions.
- The permutation feature importance values can be used to compare different models.
- The permutation feature importance values can be used to identify which features are most important for the model's predictions.
""")
st.markdown("### Conclusion:")
st.markdown("""
- The model's performance can be evaluated using various metrics such as R^2 score, MAE, MSE, and RMSE.
- The confusion matrix provides insights into the model's classification performance.
- The feature importance values can help identify which features are most important for the model's predictions.
""")