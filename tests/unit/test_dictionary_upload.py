import os
import io
import pytest
import pandas as pd


REQUIRED_COLUMNS = {"b5t", "keywords"}


def save_dictionary(file_obj, upload_folder):
    """Simulates saving a dictionary file after column check."""
    os.makedirs(upload_folder, exist_ok=True)
    dict_path = os.path.join(upload_folder, "dictionary.csv")
    
    df = pd.read_csv(file_obj)
    df.columns = [col.lower() for col in df.columns]

    if set(df.columns) != REQUIRED_COLUMNS:
        raise ValueError("CSV must contain exactly these columns: b5t, keywords")

    # Delete existing CSV files
    for f in os.listdir(upload_folder):
        if f.endswith(".csv"):
            os.remove(os.path.join(upload_folder, f))

    df.to_csv(dict_path, index=False)
    return dict_path


def load_dictionary(dict_path):
    """Loads the saved dictionary for checking stats."""
    if not os.path.exists(dict_path):
        raise FileNotFoundError("Dictionary file does not exist.")
    return pd.read_csv(dict_path)


@pytest.fixture
def sample_csv_bytesio():
    return io.BytesIO(b"b5t,keywords\nGreeting,hello\nConfirming,yes")


@pytest.fixture
def bad_csv_bytesio():
    return io.BytesIO(b"category,terms\nBad,test")


def test_save_and_load_dictionary(tmp_path, sample_csv_bytesio):
    upload_folder = tmp_path / "uploaded_dictionaries"
    sample_csv_bytesio.seek(0)
    path = save_dictionary(sample_csv_bytesio, str(upload_folder))

    # Check if file was saved
    assert os.path.exists(path)

    # Load and verify
    df = load_dictionary(path)
    assert set(df.columns) == REQUIRED_COLUMNS
    assert df.shape == (2, 2)
    assert "Greeting" in df["b5t"].values


def test_save_dictionary_invalid_format(tmp_path, bad_csv_bytesio):
    upload_folder = tmp_path / "uploaded_dictionaries"
    bad_csv_bytesio.seek(0)

    with pytest.raises(ValueError, match="CSV must contain exactly these columns"):
        save_dictionary(bad_csv_bytesio, str(upload_folder))


def test_load_dictionary_missing_file(tmp_path):
    fake_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        load_dictionary(str(fake_path))
