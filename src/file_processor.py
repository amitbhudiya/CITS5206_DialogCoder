import pandas as pd
from classifier import classify_sentence, get_b5t_and_subcategories

# Read CSV file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Process uploaded CSV file
def process_uploaded_csv(input_path, output_path):
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        raise Exception("File not found")
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