import os
import unittest
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from file_processor import process_single_file, process_multi_files


class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        """Prepare the testing environment: define input and output paths."""
        # get the path of the test file
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(self.test_dir, "../.."))
        self.sample_files = os.path.join(self.project_root, "tests/sample_files")
        
        # create the output directory
        self.output_dir = os.path.join(self.project_root, "tests/output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Single file testing
        self.single_input = os.path.join(self.sample_files, "test.csv")
        self.single_output = os.path.join(self.output_dir, "output.csv")

        # Multiple files batch testing
        self.batch_input = [self.single_input, self.single_input]
        self.batch_output = [
            os.path.join(self.output_dir, "output1.csv"),
            os.path.join(self.output_dir, "output2.csv")
        ]

        # Folder batch testing
        self.batch_folder = os.path.join(self.sample_files, "batch")
        self.batch_output_folder = os.path.join(self.output_dir, "batch_output")

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
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.batch_output_folder)
            
        # if the output directory exists and is empty, delete it
        if os.path.exists(self.output_dir) and not os.listdir(self.output_dir):
            os.rmdir(self.output_dir)

    def test_process_single_file(self):
        """Test processing a single CSV file."""
        process_single_file(self.single_input, self.single_output)

        # Check if the output file exists
        self.assertTrue(
            os.path.exists(self.single_output), "Single output file was not created."
        )

        # Validate the content of the output
        df = pd.read_csv(self.single_output)
        self.assertIn("B5T", df.columns, "'B5T' column is missing in the output.")
        self.assertGreater(len(df), 0, "The output file contains no rows.")

    def test_batch_processing(self):
        """Test processing multiple CSV files (batch processing)."""
        process_multi_files(self.batch_input, self.batch_output)

        for out_file in self.batch_output:
            # Check if each batch output file exists
            self.assertTrue(
                os.path.exists(out_file),
                f"Batch output file {out_file} was not created.",
            )

            # Validate the content of each batch output file
            df = pd.read_csv(out_file)
            self.assertIn("B5T", df.columns, "'B5T' column is missing in batch output.")
            self.assertGreater(len(df), 0, "A batch output file contains no rows.")

    def test_folder_processing(self):
        """Test processing all CSV files inside a folder."""
        os.makedirs(self.batch_output_folder, exist_ok=True)

        # Assert that batch input folder exists before processing
        self.assertTrue(
            os.path.isdir(self.batch_folder), "Batch input folder does not exist!"
        )

        process_multi_files(self.batch_folder, self.batch_output_folder)

        input_files = [f for f in os.listdir(self.batch_folder) if f.endswith(".csv")]

        for file in input_files:
            output_file = os.path.join(self.batch_output_folder, file)

            # Check if the output file for each input file exists
            self.assertTrue(
                os.path.exists(output_file),
                f"Folder output file {output_file} was not created.",
            )

            # Validate the content of each output file
            df = pd.read_csv(output_file)
            self.assertIn(
                "B5T", df.columns, "'B5T' column is missing in folder output."
            )
            self.assertGreater(len(df), 0, "A folder output file contains no rows.")


if __name__ == "__main__":
    unittest.main()
