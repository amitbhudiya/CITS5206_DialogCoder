"""
TODO MVP v0.1
"""

import tempfile
from pathlib import Path

import pandas as pd


class Exporter:
    """Handles exporting of results to various formats."""

    def __init__(self):
        pass

    def export_to_csv(self, data, filename):
        """
        Export data to CSV file.

        Args:
            data: Data to export (DataFrame or compatible structure)
            filename: Target filename for export

        Returns:
            Boolean indicating success or failure
        """

    def export_to_json(self, data, filename):
        """
        Export data to JSON file.

        Args:
            data: Data to export
            filename: Target filename for export

        Returns:
            Boolean indicating success or failure
        """


def export_csv(df: pd.DataFrame, original_name: str) -> Path:
    """
    Export a DataFrame to CSV in a temporary directory with a modified filename.

    Args:
        df: The pandas DataFrame to export
        original_name: The original filename or path to base the new filename on

    Returns:
        Path object pointing to the exported CSV file

    Example:
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        >>> path = export_csv(df, "my_data.xlsx")
        >>> path.name
        'my_data_coded.csv'
    """
    # Create temporary directory if it doesn't exist
    tmp_dir = Path(tempfile.gettempdir())

    # Extract the stem (filename without extension) from the original name
    original_path = Path(original_name)
    original_stem = original_path.stem

    # Create the new filename with "_coded" suffix
    output_filename = f"{original_stem}_coded.csv"
    output_path = tmp_dir / output_filename

    # Save the DataFrame to CSV with UTF-8 encoding and no index
    df.to_csv(output_path, index=False, encoding="utf-8")

    return output_path
