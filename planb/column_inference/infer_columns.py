"""
TODO MVP v0.1
"""

from typing import Tuple

import pandas as pd


class ColumnInference:
    """Analyzes and infers column roles and types from data."""

    def __init__(self):
        pass

    def infer_columns(self, dataframe):
        """
        Analyze dataframe to infer column roles and types.

        Args:
            dataframe: pandas DataFrame to analyze

        Returns:
            Dictionary of column metadata with inferred types and roles
        """


def infer_dictionary_columns(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Return hardcoded column names for keywords and codes.

    This function no longer attempts to infer column names, but instead
    returns fixed column names that should be used throughout the system.
    If the provided columns don't exist in the dataframe, it attempts
    to use common alternatives or raises a clear error.

    Args:
        df: DataFrame to check for expected columns

    Returns:
        Tuple of (keyword_column_name, code_column_name)

    Raises:
        ValueError: If required columns cannot be found
    """
    # Define expected column names
    expected_keyword_col = "keywords"
    expected_code_col = "classification_code"

    # Check if the expected columns exist
    if expected_keyword_col in df.columns and expected_code_col in df.columns:
        return expected_keyword_col, expected_code_col

    # Alternative column names
    keyword_alternatives = ["keyword", "term", "phrase", "text", "word", "expression"]
    code_alternatives = [
        "code",
        "id",
        "label",
        "classification",
        "category",
        "class",
        "type",
    ]

    # Try to find matching columns
    keyword_col = None
    for alt in keyword_alternatives:
        if alt in df.columns:
            keyword_col = alt
            break

    code_col = None
    for alt in code_alternatives:
        if alt in df.columns:
            code_col = alt
            break

    # If alternatives are found, use them
    if keyword_col is not None and code_col is not None:
        return keyword_col, code_col

    # If we still don't have columns, try to use the first two columns
    if len(df.columns) >= 2:
        return df.columns[0], df.columns[1]

    # If all else fails, raise an error
    raise ValueError(
        f"Could not find required columns. Expected '{expected_keyword_col}' and '{expected_code_col}'. "
        f"Please rename your columns or restructure your data."
    )
