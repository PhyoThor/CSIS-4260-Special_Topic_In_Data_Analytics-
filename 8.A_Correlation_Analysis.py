import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the merged stock-news dataset
file_path = "./.venv/data/apple_stock_news_merged.csv"
df = pd.read_csv(file_path, parse_dates=["Date"])

# Drop non-numeric columns for correlation analysis
numeric_df = df.select_dtypes(include=["number"])

# Compute correlation matrix
correlation_matrix = numeric_df.corr()

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True, linewidths=0.5)
plt.title(" Correlation Matrix - Apple Stock & News Features", fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
