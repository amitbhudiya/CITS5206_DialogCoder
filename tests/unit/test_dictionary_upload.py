"""
Unit tests for dictionary upload functionality.
"""

import io
from unittest.mock import patch

import pandas as pd
import pytest

# Import the functions to test
# Assuming these are in app.services.dictionary or similar - adjust as needed
# from app.services.dictionary import save_dictionary, load_dictionary


@pytest.fixture
def sample_csv_content():
    """Return sample CSV content for testing."""
    return "keyword,category\n" "request,Requesting\n" "confirm,Confirming\n"


@pytest.fixture
def sample_csv_file(tmp_path, sample_csv_content):
    """Create a sample CSV file in the temp directory."""
    file_path = tmp_path / "test_dict.csv"
    with open(file_path, "w") as f:
        f.write(sample_csv_content)
    return file_path


@pytest.fixture
def sample_csv_bytesio(sample_csv_content):
    """Return a BytesIO object containing sample CSV data."""
    return io.BytesIO(sample_csv_content.encode("utf-8"))


@patch("app.settings.DICT_DIR")
def test_save_dictionary_writes_file(mock_dict_dir, tmp_path, sample_csv_bytesio):
    """
    Test that save_dictionary writes the file to the correct location with expected content.

    Args:
        mock_dict_dir: Mocked settings.DICT_DIR
        tmp_path: Pytest fixture that provides a temporary directory
        sample_csv_bytesio: BytesIO containing sample CSV data
    """
    from app.services.dictionary import save_dictionary

    # Set the dictionary directory to our temp path
    mock_dict_dir.return_value = tmp_path

    # Test user ID
    user_id = "test_user_123"

    # Reset file position to start
    sample_csv_bytesio.seek(0)

    # Call the function
    result_path = save_dictionary(file=sample_csv_bytesio, user_id=user_id)

    # Assert the returned path matches expected
    expected_path = tmp_path / f"{user_id}.csv"
    assert result_path == expected_path

    # Assert the file exists
    assert expected_path.exists()

    # Assert the content matches
    with open(expected_path, "r") as f:
        content = f.read()
        sample_csv_bytesio.seek(0)
        expected_content = sample_csv_bytesio.read().decode("utf-8")
        assert content == expected_content


@patch("app.settings.DICT_DIR")
def test_load_dictionary_returns_frame(mock_dict_dir, tmp_path, sample_csv_file):
    """
    Test that load_dictionary correctly loads a CSV file into a DataFrame.

    Args:
        mock_dict_dir: Mocked settings.DICT_DIR
        tmp_path: Pytest fixture that provides a temporary directory
        sample_csv_file: Path to sample CSV file
    """
    from app.services.dictionary import load_dictionary

    # Set the dictionary directory to our temp path
    mock_dict_dir.return_value = tmp_path

    # Test user ID - should match the filename in tmp_path
    user_id = "test_user_123"

    # Copy the sample file to the expected location
    target_path = tmp_path / f"{user_id}.csv"
    with open(sample_csv_file, "r") as src, open(target_path, "w") as dst:
        dst.write(src.read())

    # Call the function
    result_df = load_dictionary(user_id=user_id)

    # Assert result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Assert dataframe has expected shape (2 rows, 2 columns)
    assert result_df.shape == (2, 2)

    # Assert column names are as expected
    expected_columns = ["keyword", "category"]
    assert list(result_df.columns) == expected_columns

    # Assert specific cell values
    assert result_df.iloc[0, 0] == "request"  # First row, keyword column
    assert result_df.iloc[0, 1] == "Requesting"  # First row, category column
    assert result_df.iloc[1, 0] == "confirm"  # Second row, keyword column
    assert result_df.iloc[1, 1] == "Confirming"  # Second row, category column


# Additional test for error handling
@patch("app.settings.DICT_DIR")
def test_load_dictionary_missing_file(mock_dict_dir, tmp_path):
    """
    Test that load_dictionary raises appropriate error when the file doesn't exist.
    """
    from app.services.dictionary import load_dictionary

    # Set the dictionary directory to our temp path
    mock_dict_dir.return_value = tmp_path

    # Use a user_id that doesn't have a file
    user_id = "nonexistent_user"

    # Assert the function raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_dictionary(user_id=user_id)
