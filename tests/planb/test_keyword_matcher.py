"""
Unit tests for the keyword matcher functionality.
"""

import pandas as pd
import pytest

from planb.pipeline.keyword_matcher import keyword_match


def test_basic_word_matching():
    """Test basic single word matching functionality."""
    # Setup test data
    row = pd.Series({"text": "I want to cancel my subscription"})
    kw_df = pd.DataFrame(
        {"keyword": ["cancel", "subscription"], "code": ["CANCEL", "SUBSCRIPTION"]}
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results
    assert len(results) == 2
    assert ("CANCEL", 1.0) in results
    assert ("SUBSCRIPTION", 1.0) in results


def test_phrase_matching():
    """Test phrase matching functionality."""
    # Setup test data
    row = pd.Series({"text": "I need to cancel my subscription plan immediately"})
    kw_df = pd.DataFrame(
        {
            "keyword": ["cancel my subscription", "immediately"],
            "code": ["CANCEL_SUBSCRIPTION", "URGENT"],
        }
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results
    assert len(results) == 2
    assert ("CANCEL_SUBSCRIPTION", 1.0) in results
    assert ("URGENT", 1.0) in results


def test_case_insensitivity():
    """Test case insensitivity of matching."""
    # Setup test data
    row = pd.Series({"text": "I want to CANCEL my Subscription"})
    kw_df = pd.DataFrame(
        {"keyword": ["cancel", "subscription"], "code": ["CANCEL", "SUBSCRIPTION"]}
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results
    assert len(results) == 2
    assert ("CANCEL", 1.0) in results
    assert ("SUBSCRIPTION", 1.0) in results


def test_whole_word_matching():
    """Test that only whole words are matched, not partial words."""
    # Setup test data
    row = pd.Series({"text": "I want to cancel my cancelation subscription"})
    kw_df = pd.DataFrame(
        {
            "keyword": ["cancel", "cancelled", "can"],
            "code": ["CANCEL", "CANCELLED", "CAN"],
        }
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results
    assert len(results) == 1
    assert ("CANCEL", 1.0) in results
    assert ("CANCELLED", 1.0) not in results
    assert ("CAN", 1.0) not in results


def test_speaker_role_placeholder():
    """Test that speaker roles are recognized (placeholder test)."""
    # Setup test data
    row = pd.Series({"text": "I want to cancel my subscription", "speaker": "customer"})
    kw_df = pd.DataFrame(
        {"keyword": ["cancel", "subscription"], "code": ["CANCEL", "SUBSCRIPTION"]}
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results - without implementation just check basic functionality works
    assert len(results) == 2
    assert ("CANCEL", 1.0) in results
    assert ("SUBSCRIPTION", 1.0) in results


def test_missing_text_column():
    """Test that an exception is raised when 'text' column is missing."""
    # Setup test data
    row = pd.Series(
        {"content": "I want to cancel my subscription"}
    )  # 'content' instead of 'text'
    kw_df = pd.DataFrame(
        {"keyword": ["cancel", "subscription"], "code": ["CANCEL", "SUBSCRIPTION"]}
    )

    # Run the function and check for exception
    with pytest.raises(ValueError, match="must contain a 'text' column"):
        keyword_match(row, kw_df)


def test_missing_keyword_code_columns():
    """Test that an exception is raised when required columns are missing in kw_df."""
    # Setup test data
    row = pd.Series({"text": "I want to cancel my subscription"})
    kw_df = pd.DataFrame(
        {
            "word": ["cancel", "subscription"],  # 'word' instead of 'keyword'
            "code": ["CANCEL", "SUBSCRIPTION"],
        }
    )

    # Run the function and check for exception
    with pytest.raises(ValueError, match="must contain 'keyword' and 'code' columns"):
        keyword_match(row, kw_df)


def test_no_matches():
    """Test behavior when no matches are found."""
    # Setup test data
    row = pd.Series({"text": "I am just saying hello"})
    kw_df = pd.DataFrame(
        {"keyword": ["cancel", "subscription"], "code": ["CANCEL", "SUBSCRIPTION"]}
    )

    # Run the function
    results = keyword_match(row, kw_df)

    # Check results
    assert len(results) == 0
