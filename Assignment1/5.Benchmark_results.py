import pandas as pd
import time
import os
import csv

# Define CSV File to Save Benchmark Results
BENCHMARK_FILE = "benchmark_results.csv"

# Function to measure read/write speed together
def benchmark_read_write(file_path_csv, file_path_parquet, dataset_name):
    print(f"\nBenchmarking {dataset_name}...")

    # Read CSV
    start_csv_read = time.time()
    df_csv = pd.read_csv(file_path_csv)
    end_csv_read = time.time()
    csv_read_time = end_csv_read - start_csv_read
    print(f"CSV Read Time: {csv_read_time:.4f} seconds")

    # Read Parquet
    start_parquet_read = time.time()
    df_parquet = pd.read_parquet(file_path_parquet)
    end_parquet_read = time.time()
    parquet_read_time = end_parquet_read - start_parquet_read
    print(f"Parquet Read Time: {parquet_read_time:.4f} seconds")

    # Write CSV
    start_csv_write = time.time()
    df_csv.to_csv(file_path_csv, index=False)
    end_csv_write = time.time()
    csv_write_time = end_csv_write - start_csv_write
    print(f"CSV Write Time: {csv_write_time:.4f} seconds")

    # Write Parquet
    start_parquet_write = time.time()
    df_csv.to_parquet(file_path_parquet, engine="pyarrow", compression="snappy")
    end_parquet_write = time.time()
    parquet_write_time = end_parquet_write - start_parquet_write
    print(f"Parquet Write Time: {parquet_write_time:.4f} seconds")

    # Save Benchmark Results
    save_benchmark_results(dataset_name, "CSV", "Read", csv_read_time)
    save_benchmark_results(dataset_name, "Parquet", "Read", parquet_read_time)
    save_benchmark_results(dataset_name, "CSV", "Write", csv_write_time)
    save_benchmark_results(dataset_name, "Parquet", "Write", parquet_write_time)

# Initialize Benchmarking Results File
def init_benchmark_file():
    with open(BENCHMARK_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset", "Library", "Operation", "Time (Seconds)"])

# Save Benchmark Results
def save_benchmark_results(dataset, file_format, operation, time_taken):
    with open(BENCHMARK_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([dataset, file_format, operation, round(time_taken, 4)])

# Main Execution
if __name__ == "__main__":
    print("\nOptimized Benchmarking Read & Write Times")

    # Initialize the benchmark results file
    init_benchmark_file()

    # List of datasets to benchmark
    datasets = [
        ("all_stocks_5yr.csv", "all_stocks_5yr.parquet", "1x"),
        ("all_stocks_5yr_10x.csv", "all_stocks_5yr_10x.parquet", "10x"),
        ("all_stocks_5yr_100x.csv", "all_stocks_5yr_100x.parquet", "100x"),
    ]

    for csv_file, parquet_file, dataset_name in datasets:
        benchmark_read_write(csv_file, parquet_file, dataset_name)

    print("\nBenchmarking Completed! Results saved in 'benchmark_results.csv'.")
