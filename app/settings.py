# app/settings.py

import os

# Absolute path to the dictionary upload folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploaded_dictionaries")

# Path to main dictionary CSV file
DICT_PATH = os.path.join(UPLOAD_FOLDER, "dictionary.csv")

# Required columns for a valid dictionary
REQUIRED_COLUMNS = {"b5t", "keywords"}
