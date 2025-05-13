"""
TODO MVP v0.1
"""

from typing import Any, Dict, List, Tuple, Union


class Aggregator:
    """Aggregates results from multiple pipeline components."""

    def __init__(self):
        pass

    def aggregate(self, results):
        """
        Combine and prioritize results from multiple pipeline components.

        Args:
            results: List of results from different pipeline components

        Returns:
            Aggregated and prioritized result
        """


def aggregate(
    keyword_hits: List[Tuple[str, float]], llm_json: Dict[str, Any], threshold: float
) -> Dict[str, Union[str, float, None]]:
    """
    Aggregate results from keyword matching and LLM classification.

    Args:
        keyword_hits: List of tuples (code, confidence) from keyword matching
        llm_json: Dictionary with LLM classification results including 'code' and 'confidence'
        threshold: Minimum confidence threshold for considering a candidate

    Returns:
        Dictionary containing:
            - primary_code: Code with highest confidence or None if none meet threshold
            - primary_confidence: Confidence of primary code (0.0 if none meet threshold)
            - secondary_code: Second highest confidence code if different from primary and >= threshold
            - secondary_confidence: Confidence of secondary code (0.0 if none qualify)
            - explanation: Explanation for the decision (from LLM if available)
    """
    # Initialize result structure
    result = {
        "primary_code": None,
        "primary_confidence": 0.0,
        "secondary_code": None,
        "secondary_confidence": 0.0,
        "explanation": None,
    }

    # Build combined candidate list
    candidates = []

    # Add keyword hits to candidates
    for code, confidence in keyword_hits:
        candidates.append({"code": code, "confidence": confidence, "source": "keyword"})

    # Add LLM result to candidates if it has required fields
    if isinstance(llm_json, dict) and "code" in llm_json and "confidence" in llm_json:
        # Extract explanation if available
        explanation = llm_json.get("explanation", None)

        # Add LLM candidate
        candidates.append(
            {
                "code": llm_json["code"],
                "confidence": float(llm_json["confidence"]),
                "source": "llm",
                "explanation": explanation,
            }
        )

    # Sort candidates by confidence in descending order
    candidates.sort(key=lambda x: x["confidence"], reverse=True)

    # Filter candidates that meet threshold
    valid_candidates = [c for c in candidates if c["confidence"] >= threshold]

    # If we have at least one valid candidate
    if valid_candidates:
        # Set primary (highest confidence)
        result["primary_code"] = valid_candidates[0]["code"]
        result["primary_confidence"] = valid_candidates[0]["confidence"]

        # Get explanation from LLM result if available
        llm_candidates = [c for c in valid_candidates if c["source"] == "llm"]
        if llm_candidates and "explanation" in llm_candidates[0]:
            result["explanation"] = llm_candidates[0]["explanation"]

        # If we have at least two valid candidates and second is different from first
        if (
            len(valid_candidates) > 1
            and valid_candidates[1]["code"] != valid_candidates[0]["code"]
        ):
            result["secondary_code"] = valid_candidates[1]["code"]
            result["secondary_confidence"] = valid_candidates[1]["confidence"]

    return result
