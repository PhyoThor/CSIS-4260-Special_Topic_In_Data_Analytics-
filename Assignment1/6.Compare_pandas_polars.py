import pandas as pd
import polars as pl
import time

# Function to measure read time
def benchmark_read(file_path, library="pandas"):
    print(f"\n Reading {file_path} using {library}...")

    start_time = time.time()
    
    if library == "pandas":
        df = pd.read_csv(file_path)
    elif library == "polars":
        df = pl.read_csv(file_path)
    
    end_time = time.time()
    print(f" {library.upper()} Read Time: {end_time - start_time:.4f} seconds")
    return df

if __name__ == "__main__":
    print("\n Comparing Pandas vs. Polars")

datasets = [
    "all_stocks_5yr.csv",
    "all_stocks_5yr_10x.csv",
    "all_stocks_5yr_100x.csv",
]

# Run benchmarks for each dataset
for dataset in datasets:
    df_pandas = benchmark_read(dataset, "pandas")
    df_polars = benchmark_read(dataset, "polars")

#  Comparing Pandas vs. Polars

#  Reading all_stocks_5yr.csv using pandas...
#  PANDAS Read Time: 0.3878 seconds

#  Reading all_stocks_5yr.csv using polars...
#  POLARS Read Time: 0.0782 seconds

#  Reading all_stocks_5yr_10x.csv using pandas...      
#  PANDAS Read Time: 3.1652 seconds

#  Reading all_stocks_5yr_10x.csv using polars...
#  POLARS Read Time: 0.4430 seconds

#  Reading all_stocks_5yr_100x.csv using pandas...
#  PANDAS Read Time: 55.0651 seconds

#  Reading all_stocks_5yr_100x.csv using polars...
#  POLARS Read Time: 6.9687 seconds


