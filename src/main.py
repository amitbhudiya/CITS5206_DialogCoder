from file_processor import process_uploaded_csv

def main():
    input_path = "./data/test.csv"
    output_path = "./data/output.csv"
    process_uploaded_csv(input_path, output_path)

if __name__ == "__main__":
    main()