import pandas as pd
import os
import logging
from src.classifier import classify_sentence, get_b5t_and_subcategories
from typing import Union, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    # 支持常见的text列名
    for col in df.columns:
        if col.strip().lower() == 'text':
            return col
    raise ValueError("CSV must contain a 'text' column (case-insensitive)")

# Process uploaded single CSV file
def process_single_file(input_file: str, output_file: str):
    """Process a single CSV file."""
    df = read_csv(input_file)
    text_col = get_text_column(df)

    results = []
    for text in df[text_col]:
        if pd.isna(text):
            continue
        categories = classify_sentence(str(text).strip())
        b5t, sub1, sub2 = get_b5t_and_subcategories(categories)
        results.append({
            'Text': text,
            'B5T': b5t,
            'Subcategory1': sub1,
            'Subcategory2': sub2
        })

    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)
    logging.info(f"Processed {len(results)} rows from {input_file}. Output saved to {output_file}")

# Process uploaded CSV files or folders
def process_uploaded_csv(input_path: Union[str, List[str]], output_path: Union[str, List[str]]):
    if isinstance(input_path, list):
        if not isinstance(output_path, list) or len(input_path) != len(output_path):
            raise ValueError("When input_path is a list, output_path must be a list of the same length.")
        for in_file, out_file in zip(input_path, output_path):
            process_single_file(in_file, out_file)
        return

    if os.path.isdir(input_path):
        if not os.path.isdir(output_path):
            raise ValueError("When input_path is a folder, output_path must be a folder.")
        for file in os.listdir(input_path):
            if file.endswith('.csv'):
                in_file = os.path.join(input_path, file)
                out_file = os.path.join(output_path, file)
                process_single_file(in_file, out_file)
        return

    # Single file case
    process_single_file(input_path, output_path)
