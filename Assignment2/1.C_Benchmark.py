# 1.C_Benchmark.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Get current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# CSV paths
reddit_csv = os.path.join(script_dir, "nvidia_praw_posts.csv")
cnn_csv = os.path.join(script_dir, "nvidia_cnn_bing.csv")

# Load data
df_reddit = pd.read_csv(reddit_csv)
df_cnn = pd.read_csv(cnn_csv)

# Measured times
reddit_time = 1.75
cnn_time = 31.78

# Build benchmark table
benchmark_data = {
    "Metric": [
        "Execution Time (s)",
        "Total Posts Fetched",
        "Data Yield (%)",
        "Cleaning Required (1–5)",
        "Scalability (1–5)",
        "Error Resilience (1–5)",
        "Topic Precision (1–5)",
        "Source Stability (1–5)"
    ],
    "Reddit (PRAW)": [
        f"{reddit_time:.2f}",
        len(df_reddit),
        "100%",
        2,
        5,
        5,
        4,
        5
    ],
    "CNN via Bing (BS4)": [
        f"{cnn_time:.2f}",
        len(df_cnn),
        "94%",
        3,
        3,
        3,
        5,
        3
    ]
}

df_benchmark = pd.DataFrame(benchmark_data)

# Save benchmark table
benchmark_md = os.path.join(script_dir, "benchmark_table.md")
df_benchmark.to_markdown(benchmark_md, index=False)

print("✅ Benchmark Table:\n")
print(df_benchmark.to_markdown(index=False))

# ----- 🔽 Chart Section Begins Here 🔽 -----

# Chart metrics to visualize
metrics = [
    "Execution Time (s)",
    "Total Posts",
    "Scalability",
    "Error Resilience",
    "Topic Precision",
    "Source Stability"
]

reddit_scores = [reddit_time, len(df_reddit), 5, 5, 4, 5]
bs4_scores = [cnn_time, len(df_cnn), 3, 3, 5, 3]

x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, reddit_scores, width, label='Reddit (PRAW)', color='royalblue')
bars2 = ax.bar(x + width/2, bs4_scores, width, label='CNN via Bing (BS4)', color='mediumseagreen')

# Labels & formatting
ax.set_ylabel('Scores / Values')
ax.set_title('Benchmark Comparison: Reddit (PRAW) vs CNN (BS4)')
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=15, ha='right')
ax.legend()

# Annotate bars
def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}' if height != int(height) else f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

annotate_bars(bars1)
annotate_bars(bars2)

plt.tight_layout()

# Save and show chart
chart_path = os.path.join(script_dir, "benchmark_comparison_chart.png")
plt.savefig(chart_path)
plt.show()
