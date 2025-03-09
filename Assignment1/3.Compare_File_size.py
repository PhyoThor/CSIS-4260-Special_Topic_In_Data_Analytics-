import os

# Function to check file size
def compare_file_sizes(csv_file, parquet_file):
    csv_size = os.path.getsize(csv_file) / (1024 * 1024)  # Convert to MB
    parquet_size = os.path.getsize(parquet_file) / (1024 * 1024)  # Convert to MB

    print(f"\n {csv_file} Size: {csv_size:.2f} MB")
    print(f" {parquet_file} Size: {parquet_size:.2f} MB")
    print(f" Compression Ratio: {parquet_size / csv_size:.2%} (Lower is better)")

if __name__ == "__main__":
    compare_file_sizes("all_stocks_5yr.csv", "all_stocks_5yr.parquet")
    compare_file_sizes("all_stocks_5yr_10x.csv", "all_stocks_5yr_10x.parquet")
    compare_file_sizes("all_stocks_5yr_100x.csv", "all_stocks_5yr_100x.parquet")

#  all_stocks_5yr.csv Size: 28.80 MB
#  all_stocks_5yr.parquet Size: 10.15 MB
#  Compression Ratio: 35.25% (Lower is better)

#  all_stocks_5yr_10x.csv Size: 288.01 MB
#  all_stocks_5yr_10x.parquet Size: 95.35 MB
#  Compression Ratio: 33.11% (Lower is better)

#  all_stocks_5yr_100x.csv Size: 2880.05 MB
#  all_stocks_5yr_100x.parquet Size: 951.67 MB
#  Compression Ratio: 33.04% (Lower is better)
