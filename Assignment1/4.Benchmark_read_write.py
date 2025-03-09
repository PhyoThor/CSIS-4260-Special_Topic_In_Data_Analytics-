import pandas as pd
import time
import os

# Function to measure read speed
def benchmark_read_time(file_path, file_format):
    print(f"\n Reading {file_path} ({file_format})...")

    start_time = time.time()
    
    if file_format == "csv":
        df = pd.read_csv(file_path)
    elif file_format == "parquet":
        df = pd.read_parquet(file_path)
    
    end_time = time.time()
    print(f" {file_format.upper()} Read Time: {end_time - start_time:.4f} seconds")
    return df

# Function to measure write speed
def benchmark_write_time(df, file_path, file_format, compression=None):
    print(f"\n Writing {file_path} ({file_format})...")

    start_time = time.time()

    if file_format == "csv":
        df.to_csv(file_path, index=False)
    elif file_format == "parquet":
        df.to_parquet(file_path, engine="pyarrow", compression=compression)

    end_time = time.time()
    print(f" {file_format.upper()} Write Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    print("\n Benchmarking Read & Write Times")

    # List of files to benchmark
    datasets = [
        ("all_stocks_5yr.csv", "all_stocks_5yr.parquet"),
        ("all_stocks_5yr_10x.csv", "all_stocks_5yr_10x.parquet"),
        ("all_stocks_5yr_100x.csv", "all_stocks_5yr_100x.parquet"),
    ]

    for csv_file, parquet_file in datasets:
        # Benchmark Read Speed
        df_csv = benchmark_read_time(csv_file, "csv")
        df_parquet = benchmark_read_time(parquet_file, "parquet")

# To ask professor which file to use

        # Benchmark Write Speed
        # benchmark_write_time(df_csv, csv_file.replace(".csv", "_copy.csv"), "csv")
        # benchmark_write_time(df_csv, parquet_file.replace(".parquet", "_copy.parquet"), "parquet", "snappy")

        # Overwrite the same file
        benchmark_write_time(df_csv, csv_file, "csv")  # Overwrites the same file
        benchmark_write_time(df_csv, parquet_file, "parquet", "snappy")  # Overwrites Parquet

#  Benchmarking Read & Write Times

#  Reading all_stocks_5yr.csv (csv)...
#  CSV Read Time: 0.4424 seconds

#  Reading all_stocks_5yr.parquet (parquet)...
#  PARQUET Read Time: 0.3354 seconds

#  Writing all_stocks_5yr.csv (csv)...
#  CSV Write Time: 2.1828 seconds

#  Writing all_stocks_5yr.parquet (parquet)...
#  PARQUET Write Time: 0.4151 seconds

#  Reading all_stocks_5yr_10x.csv (csv)...
#  CSV Read Time: 3.7303 seconds

#  Reading all_stocks_5yr_10x.parquet (parquet)...
#  PARQUET Read Time: 0.8391 seconds

#  Writing all_stocks_5yr_10x.csv (csv)...
#  CSV Write Time: 22.5318 seconds

#  Writing all_stocks_5yr_10x.parquet (parquet)...
#  PARQUET Write Time: 3.7975 seconds

#  Reading all_stocks_5yr_100x.csv (csv)...
#  CSV Read Time: 69.9628 seconds

#  Reading all_stocks_5yr_100x.parquet (parquet)...
#  PARQUET Read Time: 52.9579 seconds

#  Writing all_stocks_5yr_100x.csv (csv)...
#  CSV Write Time: 250.4084 seconds

#  Writing all_stocks_5yr_100x.parquet (parquet)...
#  PARQUET Write Time: 59.5080 seconds
