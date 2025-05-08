"""
TODO MVP v0.1
"""

import re
from typing import List, Tuple

import pandas as pd


class KeywordMatcher:
    """Matches user input against predefined keywords to determine intent."""

    def __init__(self):
        pass

    def match(self, query):
        """
        Analyze input query for keywords to determine intent.

        Args:
            query: The user input text to analyze

        Returns:
            Dictionary with matched keywords and confidence scores
        """


def keyword_match(df_row: pd.Series, kw_df: pd.DataFrame) -> List[Tuple[str, float]]:
    """
    Match keywords from a keyword dataframe against text in a dataframe row.

    Args:
        df_row: A pandas Series representing a row from a dataframe,
                must contain a 'text' column
        kw_df: A pandas DataFrame containing keywords to match against,
               must have columns 'keyword' and 'code'

    Returns:
        List of tuples (code, confidence) for each keyword match found
        where code is the code from kw_df and confidence is 1.0 for direct matches

    Example:
        >>> row = pd.Series({'text': 'I want to cancel my subscription'})
        >>> kw_df = pd.DataFrame({
        ...     'keyword': ['cancel', 'subscription'],
        ...     'code': ['CANCEL', 'SUBSCRIPTION']
        ... })
        >>> keyword_match(row, kw_df)
        [('CANCEL', 1.0), ('SUBSCRIPTION', 1.0)]
    """
    if "text" not in df_row:
        raise ValueError("DataFrame row must contain a 'text' column")

    if not all(col in kw_df.columns for col in ["keyword", "code"]):
        raise ValueError("Keyword DataFrame must contain 'keyword' and 'code' columns")

    # Get the text to search in
    text = df_row["text"].lower()

    # List to store matches
    matches = []

    # Apply special role-based rules if speaker information is available
    speaker_role = None
    if "speaker" in df_row:
        speaker_role = (
            df_row["speaker"].lower() if not pd.isna(df_row["speaker"]) else None
        )

        # Placeholder for role-based rules (FR-4)
        if speaker_role == "agent":
            # Apply agent-specific rules
            pass
        elif speaker_role == "customer":
            # Apply customer-specific rules
            pass

    # Process each keyword
    for _, kw_row in kw_df.iterrows():
        keyword = kw_row["keyword"].lower()
        code = kw_row["code"]

        # Handle phrase keywords (containing spaces)
        if " " in keyword:
            # For phrases, match the entire phrase
            pattern = r"\b" + re.escape(keyword) + r"\b"
        else:
            # For single words, match whole words
            pattern = r"\b" + re.escape(keyword) + r"\b"

        # Search for the pattern in the text
        if re.search(pattern, text):
            matches.append((code, 1.0))

    return matches
