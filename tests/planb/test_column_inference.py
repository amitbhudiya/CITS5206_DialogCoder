"""
Unit tests for column inference functionality.
"""

import pandas as pd
import pytest

from planb.column_inference.infer_columns import infer_dictionary_columns


def test_preferred_column_names():
    """Test with the preferred 'keywords' and 'classification_code' columns."""
    # Setup test data with the preferred column names
    df = pd.DataFrame(
        {
            "keywords": ["cancel", "subscription", "refund", "upgrade"],
            "classification_code": ["CANCEL", "SUBSCRIPTION", "REFUND", "UPGRADE"],
        }
    )

    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)

    # Check results
    assert keyword_col == "keywords"
    assert code_col == "classification_code"


def test_standard_keyword_code_columns():
    """Test with standard 'keyword' and 'code' columns."""
    # Setup test data with common alternative column names
    df = pd.DataFrame(
        {
            "keyword": ["cancel", "subscription", "refund", "upgrade"],
            "code": ["CANCEL", "SUBSCRIPTION", "REFUND", "UPGRADE"],
        }
    )

    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)

    # Check results
    assert keyword_col == "keyword"
    assert code_col == "code"


def test_alternative_column_names():
    """Test with alternative column names from the allowed list."""
    # Setup test data with alternative column names
    df = pd.DataFrame(
        {
            "term": [
                "cancel subscription",
                "request refund",
                "upgrade plan",
                "technical support",
            ],
            "category": ["CANCEL", "REFUND", "UPGRADE", "SUPPORT"],
        }
    )

    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)

    # Check results - should match the alternative names
    assert keyword_col == "term"
    assert code_col == "category"


def test_ambiguous_column_names():
    """Test with ambiguous column names that don't match known patterns."""
    # Setup test data with ambiguous names
    df = pd.DataFrame(
        {
            "col1": [
                "cancel my subscription",
                "I want a refund",
                "upgrade my plan",
                "technical issue",
            ],
            "col2": ["CXL", "RFD", "UPG", "TECH"],
        }
    )

    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)

    # Check results - should use first two columns in order
    assert keyword_col == "col1"
    assert code_col == "col2"


def test_single_column_dataframe():
    """Test that ValueError is raised when DataFrame has only one column."""
    # Setup test data - only one column
    df = pd.DataFrame({"column_a": ["A1", "A2", "A3", "A4"]})

    # Run the function and check for proper fallback
    with pytest.raises(ValueError):
        infer_dictionary_columns(df)


def test_multiple_matching_columns():
    """Test when multiple columns match patterns - should take first match."""
    # Setup test data with multiple matching columns
    df = pd.DataFrame(
        {
            "keyword": ["cancel", "refund", "complaint"],
            "phrase": ["cancel service", "request refund", "make complaint"],
            "code": ["CXL", "RFD", "CPL"],
            "label": ["Cancel", "Refund", "Complaint"],
        }
    )

    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)

    # Check results - should take the first match in each case
    assert keyword_col == "keyword"
    assert code_col == "code"
