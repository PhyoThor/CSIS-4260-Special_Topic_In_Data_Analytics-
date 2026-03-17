"""
Upload Apple Stock Price Prediction datasets to Kaggle.

Usage:
    python upload_to_kaggle.py

Requirements:
    - kaggle Python package: pip install kaggle
    - Kaggle API credentials configured via one of:
        a) Environment variables: KAGGLE_USERNAME and KAGGLE_KEY
        b) Credentials file at ~/.kaggle/kaggle.json:
           {"username": "<your_username>", "key": "<your_api_key>"}
           (chmod 600 ~/.kaggle/kaggle.json on Linux/macOS)

    Obtain your API key from https://www.kaggle.com/settings -> API -> Create New Token.
"""

import os
import json
import shutil
import tempfile

# ---------------------------------------------------------------------------
# Dataset files to include in the Kaggle upload
# ---------------------------------------------------------------------------
DATASET_FILES = [
    "apple_stock_ml.csv",
    "apple_stock_with_indicators.csv",
    "apple_stock_enriched_phase2_output.csv",
    "apple_news_stock_enriched.csv",
    "merged_apple_news_cleaned_full.csv",
    "apple_google_news_enriched_clean_only.csv",
]

# Notebook file(s) to include alongside the datasets
NOTEBOOK_FILES = [
    "10.apple_stock_ml copy.ipynb",
]

METADATA_FILE = "dataset-metadata.json"


def _check_kaggle_credentials():
    """Verify Kaggle credentials are available before importing the API."""
    env_username = os.environ.get("KAGGLE_USERNAME")
    env_key = os.environ.get("KAGGLE_KEY")
    if env_username and env_key:
        return

    kaggle_json = os.path.expanduser("~/.kaggle/kaggle.json")
    if os.path.isfile(kaggle_json):
        return

    raise EnvironmentError(
        "Kaggle credentials not found.\n"
        "Set the KAGGLE_USERNAME and KAGGLE_KEY environment variables, or\n"
        "place your kaggle.json file at ~/.kaggle/kaggle.json.\n"
        "Get your API key at https://www.kaggle.com/settings -> API -> Create New Token."
    )


def upload_dataset(base_dir: str = None, new_dataset: bool = False):
    """
    Upload (or update) the dataset on Kaggle.

    Parameters
    ----------
    base_dir : str, optional
        Root directory of the project. Defaults to the directory containing
        this script.
    new_dataset : bool
        If True, create a brand-new dataset on Kaggle.
        If False (default), push a new version to an existing dataset.
    """
    _check_kaggle_credentials()

    # Import here so a missing package gives a clear error only when needed.
    try:
        import kaggle  # noqa: F401
        from kaggle.api.kaggle_api_extended import KaggleApiExtended
    except ImportError:
        raise ImportError(
            "The 'kaggle' package is not installed. Run: pip install kaggle"
        )

    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    metadata_path = os.path.join(base_dir, METADATA_FILE)
    if not os.path.isfile(metadata_path):
        raise FileNotFoundError(
            f"Dataset metadata file not found: {metadata_path}"
        )

    # Collect existing dataset files
    missing = [
        f for f in DATASET_FILES
        if not os.path.isfile(os.path.join(base_dir, f))
    ]
    if missing:
        print(
            "Warning: the following dataset files were not found and will be skipped:\n"
            + "\n".join(f"  {f}" for f in missing)
        )

    available = [
        f for f in DATASET_FILES
        if os.path.isfile(os.path.join(base_dir, f))
    ]
    if not available:
        raise FileNotFoundError(
            "No dataset CSV files found. Run the data pipeline first."
        )

    # Collect existing notebook files
    available_notebooks = [
        f for f in NOTEBOOK_FILES
        if os.path.isfile(os.path.join(base_dir, f))
    ]
    missing_notebooks = [
        f for f in NOTEBOOK_FILES
        if not os.path.isfile(os.path.join(base_dir, f))
    ]
    if missing_notebooks:
        print(
            "Warning: the following notebook files were not found and will be skipped:\n"
            + "\n".join(f"  {f}" for f in missing_notebooks)
        )

    # Build a temporary staging directory containing only the files to upload
    with tempfile.TemporaryDirectory() as staging_dir:
        # Copy metadata
        shutil.copy(metadata_path, os.path.join(staging_dir, METADATA_FILE))

        # Copy dataset files
        for filename in available:
            shutil.copy(
                os.path.join(base_dir, filename),
                os.path.join(staging_dir, filename),
            )

        # Copy notebook files
        for filename in available_notebooks:
            shutil.copy(
                os.path.join(base_dir, filename),
                os.path.join(staging_dir, filename),
            )

        print(f"Staging directory: {staging_dir}")
        print("Files to upload:")
        for filename in available + available_notebooks:
            size_mb = os.path.getsize(os.path.join(staging_dir, filename)) / (1024 * 1024)
            print(f"  {filename}  ({size_mb:.2f} MB)")

        api = KaggleApiExtended()
        api.authenticate()

        if new_dataset:
            print("\nCreating new Kaggle dataset ...")
            api.dataset_create_new(
                folder=staging_dir,
                convert_to_csv=False,
                dir_mode="zip",
            )
            print("Dataset created successfully.")
        else:
            print("\nPushing new version to existing Kaggle dataset ...")
            api.dataset_create_version(
                folder=staging_dir,
                version_notes="Updated dataset files",
                convert_to_csv=False,
                dir_mode="zip",
            )
            print("Dataset version uploaded successfully.")

    # Print the public dataset URL derived from the metadata
    with open(metadata_path) as f:
        meta = json.load(f)
    dataset_id = meta.get("id", "")
    if dataset_id:
        print(f"\nDataset URL: https://www.kaggle.com/datasets/{dataset_id}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Upload Apple Stock Price Prediction dataset to Kaggle."
    )
    parser.add_argument(
        "--new",
        action="store_true",
        help="Create a brand-new dataset instead of updating an existing one.",
    )
    parser.add_argument(
        "--dir",
        default=None,
        metavar="PATH",
        help="Project root directory (defaults to the script location).",
    )
    args = parser.parse_args()

    upload_dataset(base_dir=args.dir, new_dataset=args.new)
