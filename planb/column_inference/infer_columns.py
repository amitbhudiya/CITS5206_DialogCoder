"""
TODO MVP v0.1
"""

import pandas as pd
import re
from typing import Tuple, Dict, List, Set, Optional

class ColumnInference:
    """Analyzes and infers column roles and types from data."""
    
    def __init__(self):
        pass
    
    def infer_columns(self, dataframe):
        """
        Analyze dataframe to infer column roles and types.
        
        Args:
            dataframe: pandas DataFrame to analyze
            
        Returns:
            Dictionary of column metadata with inferred types and roles
        """
        pass


def infer_dictionary_columns(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Infer which columns in a dataframe likely contain keywords and codes.
    
    Uses multiple heuristics:
    - Column name token similarity to 'keyword', 'code', etc.
    - Uniqueness ratio (number of unique values / total rows)
    - Average token count (words per cell)
    
    Args:
        df: DataFrame to analyze, assumed to contain keyword and code columns
        
    Returns:
        Tuple of (keyword_column_name, code_column_name)
        
    Raises:
        ValueError: If columns cannot be confidently determined (confidence < 0.6)
    """
    # Ensure we have at least 2 columns
    if len(df.columns) < 2:
        raise ValueError("Dictionary DataFrame must have at least 2 columns")
    
    # Dictionary of column scores
    column_scores: Dict[str, Dict[str, float]] = {
        'keyword': {},
        'code': {}
    }
    
    # Keywords that suggest column type
    keyword_indicators = {'keyword', 'term', 'phrase', 'text', 'word', 'expression'}
    code_indicators = {'code', 'id', 'label', 'tag', 'category', 'class', 'type'}
    
    # Calculate scores for each column
    for col in df.columns:
        col_lower = col.lower()
        tokens = set(re.findall(r'\w+', col_lower))
        
        # Initialize scores
        column_scores['keyword'][col] = 0.0
        column_scores['code'][col] = 0.0
        
        # 1. Column name token similarity
        keyword_token_match = len(tokens.intersection(keyword_indicators))
        code_token_match = len(tokens.intersection(code_indicators))
        
        if keyword_token_match > 0:
            column_scores['keyword'][col] += 0.4
        if code_token_match > 0:
            column_scores['code'][col] += 0.4
        
        # If the column name is exactly a keyword indicator, boost score
        if col_lower in keyword_indicators:
            column_scores['keyword'][col] += 0.3
        if col_lower in code_indicators:
            column_scores['code'][col] += 0.3
        
        # 2. Uniqueness ratio - codes tend to be more unique
        if not df[col].empty:
            uniqueness_ratio = df[col].nunique() / len(df)
            # High uniqueness suggests code, medium-low suggests keyword
            if uniqueness_ratio > 0.8:
                column_scores['code'][col] += 0.2
            elif 0.01 <= uniqueness_ratio <= 0.5:
                column_scores['keyword'][col] += 0.15
        
        # 3. Average token count - keywords usually have more tokens
        if df[col].dtype == 'object':  # Only for string columns
            # Calculate average word count
            avg_token_count = df[col].astype(str).apply(lambda x: len(re.findall(r'\w+', x))).mean()
            
            if avg_token_count >= 2:
                column_scores['keyword'][col] += 0.3
            elif avg_token_count < 1.5:
                column_scores['code'][col] += 0.2
    
    # Find best columns for each role
    keyword_col = max(column_scores['keyword'].items(), key=lambda x: x[1])
    code_col = max(column_scores['code'].items(), key=lambda x: x[1])
    
    # Check confidence
    keyword_confidence = keyword_col[1]
    code_confidence = code_col[1]
    
    # Check for duplicates (same column for both roles)
    if keyword_col[0] == code_col[0]:
        # Take the role with higher confidence, find next best for the other
        if keyword_confidence > code_confidence:
            # Remove the chosen keyword column from code candidates
            del column_scores['code'][keyword_col[0]]
            if column_scores['code']:  # If there are other columns
                code_col = max(column_scores['code'].items(), key=lambda x: x[1])
            else:
                raise ValueError("Cannot distinguish between keyword and code columns")
        else:
            # Remove the chosen code column from keyword candidates
            del column_scores['keyword'][code_col[0]]
            if column_scores['keyword']:  # If there are other columns
                keyword_col = max(column_scores['keyword'].items(), key=lambda x: x[1])
            else:
                raise ValueError("Cannot distinguish between keyword and code columns")
    
    # Final confidence check
    if keyword_confidence < 0.6 or code_confidence < 0.6:
        column_info = "\n".join([f"Column '{col}': keyword score={column_scores['keyword'][col]:.2f}, "
                                f"code score={column_scores['code'][col]:.2f}" 
                                for col in df.columns])
        raise ValueError(f"Cannot confidently determine keyword and code columns. "
                        f"Confidence threshold is 0.6, but found keyword={keyword_confidence:.2f}, "
                        f"code={code_confidence:.2f}.\n"
                        f"Column scores:\n{column_info}\n"
                        f"Try renaming columns to 'keyword' and 'code', or pass them explicitly.")
    
    return keyword_col[0], code_col[0] 