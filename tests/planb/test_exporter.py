"""
Unit tests for the exporter functionality.
"""

import os
import pandas as pd
import tempfile
from pathlib import Path

from planb.persistence.exporter import export_csv


def test_export_csv_basic():
    """Test that export_csv correctly exports a DataFrame to CSV with proper naming."""
    # Setup test data
    df = pd.DataFrame({
        'text': ['Hello world', 'Test message'],
        'primary_code': ['GREETING', 'TEST'],
        'primary_confidence': [0.9, 0.8]
    })
    
    original_filename = "test_transcript.xlsx"
    
    # Run the function
    output_path = export_csv(df, original_filename)
    
    # Check results
    assert output_path.exists(), "Output file doesn't exist"
    assert output_path.name == "test_transcript_coded.csv", "Output filename is incorrect"
    
    # Verify file content
    loaded_df = pd.read_csv(output_path)
    assert len(loaded_df) == len(df), "Row count doesn't match"
    assert list(loaded_df.columns) == list(df.columns), "Columns don't match"
    assert loaded_df.iloc[0]['primary_code'] == 'GREETING', "Data content is incorrect"
    
    # Clean up
    output_path.unlink(missing_ok=True)


def test_export_csv_filename_handling():
    """Test that export_csv handles different filename formats properly."""
    # Setup minimal test data
    df = pd.DataFrame({'col1': [1]})
    
    # Test with full path
    full_path = "/path/to/some_data.csv"
    output_path = export_csv(df, full_path)
    assert output_path.name == "some_data_coded.csv"
    output_path.unlink(missing_ok=True)
    
    # Test with filename only
    filename_only = "data.csv"
    output_path = export_csv(df, filename_only)
    assert output_path.name == "data_coded.csv"
    output_path.unlink(missing_ok=True)
    
    # Test with different extension
    json_file = "data.json"
    output_path = export_csv(df, json_file)
    assert output_path.name == "data_coded.csv", "Should convert any extension to .csv"
    output_path.unlink(missing_ok=True)


def test_export_csv_with_existing_file():
    """Test that export_csv overwrites file if it already exists."""
    # Setup test data
    df1 = pd.DataFrame({'col1': [1, 2]})
    df2 = pd.DataFrame({'col1': [3, 4, 5]})  # Different content and size
    
    original_filename = "existing_test.csv"
    
    # First export
    output_path = export_csv(df1, original_filename)
    
    # Get file stats to check modification time later
    first_mod_time = output_path.stat().st_mtime
    
    # Wait a moment to ensure modification time would be different
    import time
    time.sleep(0.1)
    
    # Second export to same location
    output_path = export_csv(df2, original_filename)
    
    # Check file was overwritten
    loaded_df = pd.read_csv(output_path)
    assert len(loaded_df) == 3, "File content should match the second DataFrame"
    assert loaded_df.iloc[0]['col1'] == 3, "File content should match the second DataFrame"
    
    # Check modification time changed
    second_mod_time = output_path.stat().st_mtime
    assert second_mod_time > first_mod_time, "File wasn't updated"
    
    # Clean up
    output_path.unlink(missing_ok=True) 