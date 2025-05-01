import pandas as pd

# Read the classified CSV file, count B5T frequency, and output the report

def generate_summary_report(input_path, output_path):
    df = pd.read_csv(input_path)
    if 'B5T' not in df.columns:
        raise Exception("The 'B5T' column is missing in the CSV file")
    
    freq = df['B5T'].value_counts().reset_index()
    freq.columns = ['B5T', 'Frequency']
    freq.to_csv(output_path, index=False)
    print(f"Frequency summary report saved to {output_path}")

if __name__ == "__main__":
    input_path = "../data/output.csv"  # Assume the output file is in the data directory
    output_path = "../data/summary_report.csv"
    generate_summary_report(input_path, output_path) 