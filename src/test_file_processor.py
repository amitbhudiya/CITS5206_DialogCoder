import unittest
import os
import pandas as pd
from file_processor import process_uploaded_csv

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        """Prepare the testing environment: define input and output paths."""
        # Single file testing
        self.single_input = "./data/test.csv"
        self.single_output = "./data/output.csv"

        # Multiple files batch testing
        self.batch_input = ["./data/test.csv", "./data/test2.csv"]
        self.batch_output = ["./data/output1.csv", "./data/output2.csv"]

        # Folder batch testing
        self.batch_folder = "./data/batch"
        self.batch_output_folder = "./data/batch_output"

    def tearDown(self):
        """Clean up all generated output files and folders after tests."""
        # Remove single and batch output files
        paths = [self.single_output] + self.batch_output
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

        # Remove batch output folder
        if os.path.exists(self.batch_output_folder):
            for file in os.listdir(self.batch_output_folder):
                file_path = os.path.join(self.batch_output_folder, file)
                os.remove(file_path)
            os.rmdir(self.batch_output_folder)

    def test_process_single_file(self):
        """Test processing a single CSV file."""
        process_uploaded_csv(self.single_input, self.single_output)

        # Check if the output file exists
        self.assertTrue(os.path.exists(self.single_output), "Single output file was not created.")

        # Validate the content of the output
        df = pd.read_csv(self.single_output)
        self.assertIn('B5T', df.columns, "'B5T' column is missing in the output.")
        self.assertGreater(len(df), 0, "The output file contains no rows.")

    def test_batch_processing(self):
        """Test processing multiple CSV files (batch processing)."""
        process_uploaded_csv(self.batch_input, self.batch_output)

        for out_file in self.batch_output:
            # Check if each batch output file exists
            self.assertTrue(os.path.exists(out_file), f"Batch output file {out_file} was not created.")

            # Validate the content of each batch output file
            df = pd.read_csv(out_file)
            self.assertIn('B5T', df.columns, "'B5T' column is missing in batch output.")
            self.assertGreater(len(df), 0, "A batch output file contains no rows.")

    def test_folder_processing(self):
        """Test processing all CSV files inside a folder."""
        os.makedirs(self.batch_output_folder, exist_ok=True)

        # Assert that batch input folder exists before processing
        self.assertTrue(os.path.isdir(self.batch_folder), "Batch input folder does not exist!")

        process_uploaded_csv(self.batch_folder, self.batch_output_folder)

        input_files = [f for f in os.listdir(self.batch_folder) if f.endswith('.csv')]

        for file in input_files:
            output_file = os.path.join(self.batch_output_folder, file)

            # Check if the output file for each input file exists
            self.assertTrue(os.path.exists(output_file), f"Folder output file {output_file} was not created.")

            # Validate the content of each output file
            df = pd.read_csv(output_file)
            self.assertIn('B5T', df.columns, "'B5T' column is missing in folder output.")
            self.assertGreater(len(df), 0, "A folder output file contains no rows.")

if __name__ == "__main__":
    unittest.main()
