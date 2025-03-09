import pandas as pd
import os

# Function to scale the dataset
def scale_data(input_csv, scale_factor, output_csv):
    print(f" Creating {scale_factor}x dataset...")

    # Load original CSV
    df = pd.read_csv(input_csv)

    #Duplicate the data `scale_factor` times
    df_large = pd.concat([df] * scale_factor, ignore_index=True)

    #Save the new dataset
    df_large.to_csv(output_csv, index=False)

    print(f" {output_csv} created! Size: {os.path.getsize(output_csv) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    input_csv = "all_stocks_5yr.csv" 

    # Generate scaled versions
    scale_data(input_csv, 10, "all_stocks_5yr_10x.csv")
    scale_data(input_csv, 100, "all_stocks_5yr_100x.csv")
