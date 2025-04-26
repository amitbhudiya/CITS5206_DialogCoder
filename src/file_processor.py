import pandas as pd
import os
from classifier import classify_sentence, get_b5t_and_subcategories
from typing import Union, List

# Read CSV file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Process uploaded CSV file(s) or folder

def process_uploaded_csv(input_path: Union[str, List[str]], output_path: Union[str, List[str]]):
    """
    Supports three usages:
    1. Single file: input_path is a file path, output_path is an output file path
    2. Multiple files: input_path is a list of file paths, output_path is a list of output file paths
    3. Folder: input_path is a folder path, output_path is an output folder path
    """
    if isinstance(input_path, list):
        # Batch processing for multiple files
        if not isinstance(output_path, list) or len(input_path) != len(output_path):
            raise Exception("When input_path is a list, output_path must be a list of the same length.")
        for in_file, out_file in zip(input_path, output_path):
            process_uploaded_csv(in_file, out_file)
        return
    
    if os.path.isdir(input_path):
        # Batch processing for folder
        if not os.path.isdir(output_path):
            raise Exception("When input_path is a folder, output_path must be a folder.")
        for file in os.listdir(input_path):
            if file.endswith('.csv'):
                in_file = os.path.join(input_path, file)
                out_file = os.path.join(output_path, file)
                process_uploaded_csv(in_file, out_file)
        return

    # Single file processing
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        raise Exception(f"File not found: {input_path}")
    if 'text' not in df.columns:
        raise Exception("CSV must contain 'text' column")

    results = []
    for text in df['text']:
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
    output_df.to_csv(output_path, index=False)
    print(f"Processed {len(results)} rows. Output saved to {output_path}")