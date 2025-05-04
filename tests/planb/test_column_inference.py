"""
Unit tests for column inference functionality.
"""

import pytest
import pandas as pd
from planb.column_inference.infer_columns import infer_dictionary_columns


def test_standard_keyword_code_columns():
    """Test inference with standard 'keyword' and 'code' columns."""
    # Setup test data - standard format
    df = pd.DataFrame({
        'keyword': ['cancel', 'subscription', 'refund', 'upgrade'],
        'code': ['CANCEL', 'SUBSCRIPTION', 'REFUND', 'UPGRADE']
    })
    
    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)
    
    # Check results
    assert keyword_col == 'keyword'
    assert code_col == 'code'


def test_alternative_column_names():
    """Test inference with alternative but clear column names."""
    # Setup test data - different column names
    df = pd.DataFrame({
        'term': ['cancel subscription', 'request refund', 'upgrade plan', 'technical support'],
        'category_id': ['CANCEL', 'REFUND', 'UPGRADE', 'SUPPORT']
    })
    
    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)
    
    # Check results
    assert keyword_col == 'term'
    assert code_col == 'category_id'


def test_ambiguous_column_names_with_content_hints():
    """Test inference with ambiguous names but content that provides hints."""
    # Setup test data - ambiguous column names but content hints
    df = pd.DataFrame({
        'col1': ['cancel my subscription', 'I want a refund', 'upgrade my plan', 'technical issue'],
        'col2': ['CXL', 'RFD', 'UPG', 'TECH']
    })
    
    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)
    
    # Check results
    assert keyword_col == 'col1'
    assert code_col == 'col2'


def test_multiple_columns_with_hints():
    """Test inference with multiple columns including metadata."""
    # Setup test data - multiple columns including metadata
    df = pd.DataFrame({
        'phrase': ['cancel my subscription', 'request a refund', 'upgrade my plan'],
        'identifier': ['CXL', 'RFD', 'UPG'],
        'confidence': [0.9, 0.85, 0.78],
        'created_at': ['2023-01-01', '2023-01-02', '2023-01-03']
    })
    
    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)
    
    # Check results
    assert keyword_col == 'phrase'
    assert code_col == 'identifier'


def test_low_confidence_columns():
    """Test that ValueError is raised when column roles can't be determined with high confidence."""
    # Setup test data - truly ambiguous columns
    df = pd.DataFrame({
        'column_a': ['A1', 'A2', 'A3', 'A4'],
        'column_b': ['B1', 'B2', 'B3', 'B4']
    })
    
    # Run the function and check for exception
    with pytest.raises(ValueError, match="Cannot confidently determine keyword and code columns"):
        infer_dictionary_columns(df)


def test_single_column_dataframe():
    """Test that ValueError is raised when DataFrame has only one column."""
    # Setup test data - only one column
    df = pd.DataFrame({
        'column_a': ['A1', 'A2', 'A3', 'A4']
    })
    
    # Run the function and check for exception
    with pytest.raises(ValueError, match="must have at least 2 columns"):
        infer_dictionary_columns(df)


def test_ambiguous_column_with_same_score():
    """Test handling when two columns might be scored as the same type."""
    # Setup test data - columns that might both score high as keywords
    df = pd.DataFrame({
        'keyword': ['cancel', 'refund', 'complaint'],
        'description': ['cancel service', 'request refund', 'make complaint'],
        'code': ['CXL', 'RFD', 'CPL']
    })
    
    # Run the function
    keyword_col, code_col = infer_dictionary_columns(df)
    
    # Either 'keyword' or 'description' could be chosen, but 'code' should be the code column
    assert keyword_col in ['keyword', 'description']
    assert code_col == 'code' 