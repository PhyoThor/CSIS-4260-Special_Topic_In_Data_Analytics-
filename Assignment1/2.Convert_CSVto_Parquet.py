import pandas as pd
import time
import os

# Function to convert CSV to Parquet
def csv_to_parquet(csv_file, parquet_file, compression="snappy"):
    print(f"\n   Converting {csv_file} to {parquet_file}...")

    df = pd.read_csv(csv_file)

    start_time = time.time()
    df.to_parquet(parquet_file, engine="pyarrow", compression=compression)
    end_time = time.time()

    print(f" Parquet Save Time ({compression}): {end_time - start_time:.4f} seconds")
    print(f" Parquet File Size: {os.path.getsize(parquet_file) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    # Convert each dataset
    csv_to_parquet("all_stocks_5yr.csv", "all_stocks_5yr.parquet")
    csv_to_parquet("all_stocks_5yr_10x.csv", "all_stocks_5yr_10x.parquet")
    csv_to_parquet("all_stocks_5yr_100x.csv", "all_stocks_5yr_100x.parquet")


# Converting all_stocks_5yr.csv to all_stocks_5yr.parquet...
# Parquet Save Time (snappy): 1.0595 seconds
# Parquet File Size: 10.15 MB

# Converting all_stocks_5yr_10x.csv to all_stocks_5yr_10x.parquet...
# Parquet Save Time (snappy): 2.8382 seconds
# Parquet File Size: 95.35 MB

# Converting all_stocks_5yr_100x.csv to all_stocks_5yr_100x.parquet...
# Parquet Save Time (snappy): 58.6856 seconds
# Parquet File Size: 951.67 MB
