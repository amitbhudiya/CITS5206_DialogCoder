"""
TODO MVP v0.1
"""

import os
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm

from planb.column_inference.infer_columns import infer_dictionary_columns
from planb.pipeline.keyword_matcher import keyword_match
from planb.pipeline.llm_adapter import OpenRouterClient
from planb.pipeline.aggregator import aggregate
from planb.logging.logger import Logger


class Dispatcher:
    """Handles routing of requests and coordinates processing pipeline components."""
    
    def __init__(self):
        pass
    
    def process_request(self, data):
        """
        Process incoming data request through the appropriate pipeline.
        
        Args:
            data: The input data to be processed
            
        Returns:
            Result of the processing pipeline
        """
        pass


def run_classification(transcript_fp: str, dict_fp: str, threshold: float = 0.5) -> pd.DataFrame:
    """
    Run the full classification pipeline on a transcript file using a keyword dictionary.
    
    Args:
        transcript_fp: File path to the transcript CSV/Excel file
        dict_fp: File path to the keyword dictionary CSV/Excel file
        threshold: Confidence threshold for classification (default: 0.5)
        
    Returns:
        Pandas DataFrame with original transcript data plus classification columns:
        - primary_code, primary_confidence
        - secondary_code, secondary_confidence
        - explanation
        
    Raises:
        FileNotFoundError: If transcript or dictionary files don't exist
        ValueError: If files can't be parsed or required columns are missing
    """
    # Initialize logger
    logger = Logger()
    
    # Log start time
    start_time = datetime.now()
    logger.log_info(f"Starting classification pipeline at {start_time}")
    
    # Read files into memory
    logger.log_info(f"Reading transcript from {transcript_fp}")
    if transcript_fp.endswith('.csv'):
        transcript_df = pd.read_csv(transcript_fp)
    elif transcript_fp.endswith(('.xlsx', '.xls')):
        transcript_df = pd.read_excel(transcript_fp)
    else:
        raise ValueError(f"Unsupported transcript file format: {transcript_fp}")
    
    logger.log_info(f"Reading dictionary from {dict_fp}")
    if dict_fp.endswith('.csv'):
        dict_df = pd.read_csv(dict_fp)
    elif dict_fp.endswith(('.xlsx', '.xls')):
        dict_df = pd.read_excel(dict_fp)
    else:
        raise ValueError(f"Unsupported dictionary file format: {dict_fp}")
    
    # Log row counts
    transcript_row_count = len(transcript_df)
    dict_row_count = len(dict_df)
    logger.log_info(f"Transcript has {transcript_row_count} rows")
    logger.log_info(f"Dictionary has {dict_row_count} entries")
    
    # Infer dictionary columns
    logger.log_info("Inferring dictionary columns")
    keyword_col, code_col = infer_dictionary_columns(dict_df)
    logger.log_info(f"Using '{keyword_col}' as keyword column and '{code_col}' as code column")
    
    # Initialize the LLM client
    llm_client = OpenRouterClient()
    
    # Initialize new columns in the transcript dataframe
    transcript_df['primary_code'] = None
    transcript_df['primary_confidence'] = 0.0
    transcript_df['secondary_code'] = None
    transcript_df['secondary_confidence'] = 0.0
    transcript_df['explanation'] = None
    
    # Ensure 'text' column exists
    text_col = 'text'
    if text_col not in transcript_df.columns:
        # Try to find a suitable column
        potential_text_columns = ['content', 'transcript', 'dialogue', 'utterance', 'message']
        for col in potential_text_columns:
            if col in transcript_df.columns:
                text_col = col
                logger.log_info(f"Using '{text_col}' as the transcript text column")
                break
        else:
            raise ValueError(f"Cannot find text column in transcript. Required column 'text' or alternatives not found.")
    
    # Process each row with progress bar
    logger.log_info(f"Processing {transcript_row_count} rows with classification pipeline")
    for i, row in tqdm(transcript_df.iterrows(), total=transcript_row_count, desc="Classifying"):
        try:
            # Create a copy of the row with 'text' column for keyword matching
            row_for_matching = row.copy()
            if text_col != 'text':
                row_for_matching['text'] = row[text_col]
            
            # Step 1: Keyword matching
            kw_hits = keyword_match(row_for_matching, dict_df[[keyword_col, code_col]].rename(
                columns={keyword_col: 'keyword', code_col: 'code'}))
            
            # Step 2: LLM classification
            # Create context for LLM
            context = {
                'row_id': i,
                'transcript_row': i + 1,  # 1-indexed for human readability
                'keywords_found': [code for code, _ in kw_hits]
            }
            
            # Add speaker if available
            if 'speaker' in row and not pd.isna(row['speaker']):
                context['speaker'] = row['speaker']
            
            # Call LLM classifier
            llm_result = {}
            try:
                llm_result = llm_client.classify_line(row[text_col], context)
            except Exception as e:
                logger.log_warning(f"LLM classification failed for row {i}: {str(e)}")
            
            # Step 3: Aggregate results
            result = aggregate(kw_hits, llm_result, threshold)
            
            # Step 4: Update DataFrame with results
            transcript_df.at[i, 'primary_code'] = result['primary_code']
            transcript_df.at[i, 'primary_confidence'] = result['primary_confidence']
            transcript_df.at[i, 'secondary_code'] = result['secondary_code']
            transcript_df.at[i, 'secondary_confidence'] = result['secondary_confidence']
            transcript_df.at[i, 'explanation'] = result['explanation']
            
        except Exception as e:
            logger.log_error(f"Error processing row {i}", error=e)
            # Continue with next row rather than terminating the entire process
    
    # Log end time and stats
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.log_info(f"Classification completed at {end_time}")
    logger.log_info(f"Processed {transcript_row_count} rows in {duration:.2f} seconds ({transcript_row_count / duration if duration > 0 else 0:.2f} rows/second)")
    
    # Calculate classification stats
    classified_rows = transcript_df['primary_code'].notna().sum()
    classified_pct = (classified_rows / transcript_row_count) * 100 if transcript_row_count > 0 else 0
    logger.log_info(f"Successfully classified {classified_rows} rows ({classified_pct:.1f}%)")
    
    return transcript_df 