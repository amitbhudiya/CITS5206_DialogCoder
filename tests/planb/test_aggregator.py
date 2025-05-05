"""
Unit tests for the aggregator functionality.
"""

import pytest
from planb.pipeline.aggregator import aggregate


@pytest.mark.parametrize(
    "keyword_hits, llm_json, threshold, expected",
    [
        # Case 1: Both keyword hits and LLM result with primary and secondary
        (
            [("CANCEL", 0.8), ("BILLING", 0.6)],
            {"code": "REFUND", "confidence": 0.7, "explanation": "Customer requesting refund"},
            0.5,
            {
                "primary_code": "CANCEL",
                "primary_confidence": 0.8,
                "secondary_code": "REFUND",
                "secondary_confidence": 0.7,
                "explanation": "Customer requesting refund"
            }
        ),
        
        # Case 2: LLM result has highest confidence, keyword hit as secondary
        (
            [("CANCEL", 0.7)],
            {"code": "REFUND", "confidence": 0.9, "explanation": "Customer requesting refund"},
            0.5,
            {
                "primary_code": "REFUND",
                "primary_confidence": 0.9,
                "secondary_code": "CANCEL",
                "secondary_confidence": 0.7,
                "explanation": "Customer requesting refund"
            }
        ),
        
        # Case 3: Multiple hits of same code should not appear as secondary
        (
            [("CANCEL", 0.8), ("CANCEL", 0.7)],
            {"code": "CANCEL", "confidence": 0.6, "explanation": "Customer wants to cancel"},
            0.5,
            {
                "primary_code": "CANCEL",
                "primary_confidence": 0.8,
                "secondary_code": None,
                "secondary_confidence": 0.0,
                "explanation": "Customer wants to cancel"
            }
        ),
        
        # Case 4: Below threshold - no valid candidates
        (
            [("CANCEL", 0.4), ("BILLING", 0.3)],
            {"code": "REFUND", "confidence": 0.2, "explanation": "Low confidence"},
            0.5,
            {
                "primary_code": None,
                "primary_confidence": 0.0,
                "secondary_code": None,
                "secondary_confidence": 0.0,
                "explanation": None
            }
        ),
        
        # Case 5: Only one candidate above threshold
        (
            [("CANCEL", 0.7)],
            {"code": "REFUND", "confidence": 0.4, "explanation": "Low confidence"},
            0.5,
            {
                "primary_code": "CANCEL",
                "primary_confidence": 0.7,
                "secondary_code": None,
                "secondary_confidence": 0.0,
                "explanation": None
            }
        ),
        
        # Case 6: Empty inputs
        (
            [],
            {},
            0.5,
            {
                "primary_code": None,
                "primary_confidence": 0.0,
                "secondary_code": None,
                "secondary_confidence": 0.0,
                "explanation": None
            }
        ),
        
        # Case 7: Multiple valid candidates but only one distinct code
        (
            [("BILLING", 0.8), ("BILLING", 0.7)],
            {"code": "BILLING", "confidence": 0.9, "explanation": "Billing inquiry"},
            0.5,
            {
                "primary_code": "BILLING",
                "primary_confidence": 0.9,
                "secondary_code": None,
                "secondary_confidence": 0.0,
                "explanation": "Billing inquiry"
            }
        ),

        # Case 8: Missing LLM result but valid keyword hits
        (
            [("CANCEL", 0.8), ("BILLING", 0.7)],
            {},
            0.5,
            {
                "primary_code": "CANCEL",
                "primary_confidence": 0.8,
                "secondary_code": "BILLING",
                "secondary_confidence": 0.7,
                "explanation": None
            }
        ),
    ]
)
def test_aggregate(keyword_hits, llm_json, threshold, expected):
    """Test the aggregation function with various input scenarios."""
    result = aggregate(keyword_hits, llm_json, threshold)
    assert result == expected


def test_aggregate_with_invalid_llm_json():
    """Test handling of invalid LLM JSON format."""
    # Test with LLM JSON missing required fields
    keyword_hits = [("CANCEL", 0.8)]
    llm_json = {"some_field": "value"}  # Missing 'code' and 'confidence'
    threshold = 0.5
    
    result = aggregate(keyword_hits, llm_json, threshold)
    
    assert result["primary_code"] == "CANCEL"
    assert result["primary_confidence"] == 0.8
    assert result["secondary_code"] is None
    assert result["explanation"] is None


def test_aggregate_with_threshold_edge_cases():
    """Test the behavior at the threshold boundary."""
    # Test with confidence exactly at threshold
    keyword_hits = [("CANCEL", 0.5), ("BILLING", 0.5)]
    llm_json = {"code": "REFUND", "confidence": 0.5, "explanation": "At threshold"}
    threshold = 0.5
    
    result = aggregate(keyword_hits, llm_json, threshold)
    
    # All should be considered valid since they're exactly at threshold
    assert result["primary_code"] in ["CANCEL", "BILLING", "REFUND"]
    assert result["primary_confidence"] == 0.5
    assert result["secondary_code"] in [None, "CANCEL", "BILLING", "REFUND"]
    if result["secondary_code"]:
        assert result["secondary_confidence"] == 0.5 