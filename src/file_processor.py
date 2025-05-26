import logging
import os
from typing import List, Union

import pandas as pd

from classifier import find_b5t_labels, load_dictionaries

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Read CSV file and check for 'text' column
def read_csv(file_path: str) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to read CSV {file_path}: {str(e)}")

    return df


def get_text_column(df):
    # Support common 'text' column names
    for col in df.columns:
        if col.strip().lower() == "text":
            return col
    raise ValueError("CSV must contain a 'text' column (case-insensitive)")


# Process uploaded single CSV file
def process_single_file(input_file: str, output_file: str):
    """Process a single CSV file."""
    df = read_csv(input_file)
    text_col = get_text_column(df)

    # Load user-defined dictionary csv file
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/uploaded_dictionaries/dictionary.csv'))
    try:
        b5t_dict = load_dictionaries(file_path)
    except FileNotFoundError:
        logging.error(f"Dictionary file not found at {file_path}")
        raise FileNotFoundError("Dictionary file not found")
    except Exception as e:
        logging.error(f"Error loading dictionary: {str(e)}")
        raise Exception(f"Error loading dictionary: {str(e)}")


    results = []
    for text in df[text_col]:
        if pd.isna(text):
            continue
        # sentence = load_dictionaries(str(text).strip())
        b5t, sub1, sub2 = find_b5t_labels(b5t_dict, text)
        results.append(
            {"Text": text, "B5T": b5t, "Subcategory1": sub1, "Subcategory2": sub2}
        )

    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)
    logging.info(
        f"Processed {len(results)} rows from {input_file}. Output saved to {output_file}"
    )


# Process multiple CSV files or folders
def process_multi_files(
    input_path: Union[str, List[str]], output_path: Union[str, List[str]]
):
    if isinstance(input_path, list):
        if not isinstance(output_path, list) or len(input_path) != len(output_path):
            raise ValueError(
                "When input_path is a list, output_path must be a list of the same length."
            )
        for in_file, out_file in zip(input_path, output_path):
            process_single_file(in_file, out_file)
        return

    if os.path.isdir(input_path):
        if not os.path.isdir(output_path):
            raise ValueError(
                "When input_path is a folder, output_path must be a folder."
            )
        for file in os.listdir(input_path):
            if file.endswith(".csv"):
                in_file = os.path.join(input_path, file)
                out_file = os.path.join(output_path, file)
                process_single_file(in_file, out_file)
        return

    # Single file case
    process_single_file(input_path, output_path)
