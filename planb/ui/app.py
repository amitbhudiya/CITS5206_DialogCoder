"""
TODO MVP v0.1
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))


import os
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Tuple, Optional, Dict


from planb.controller.dispatcher import run_classification
from planb.persistence.exporter import export_csv
from planb.logging.logger import Logger

# Initialize logger
logger = Logger()

def load_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load an uploaded file into a pandas DataFrame.
    
    Args:
        uploaded_file: File uploaded through Streamlit's file_uploader
    
    Returns:
        DataFrame or None if loading fails
    """
    if uploaded_file is None:
        return None
        
    try:
        # Get file extension
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension == '.csv':
            return pd.read_csv(uploaded_file)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        logger.log_error(f"Error loading file {uploaded_file.name}", error=e)
        return None


def show_dataframe_preview(df: pd.DataFrame, n_rows: int = 30) -> None:
    """
    Display a color-coded preview of the DataFrame.
    
    Args:
        df: DataFrame to display
        n_rows: Number of rows to show
    """
    if df is None or df.empty:
        st.write("No data to display.")
        return
    
    # Get subset of DataFrame for preview
    preview_df = df.head(n_rows)
    
    # Check if classification columns exist
    if 'primary_confidence' in preview_df.columns:
        # Create a styled DataFrame with color coding based on confidence
        def highlight_confidence(row):
            styles = [''] * len(row)
            if 'primary_confidence' in row.index:
                conf = row['primary_confidence']
                if conf is not None:
                    if conf >= 0.8:
                        color = 'background-color: #c6efce'  # Green for high confidence
                    elif conf >= 0.5:
                        color = 'background-color: #ffeb9c'  # Yellow for medium confidence
                    else:
                        color = 'background-color: #ffc7ce'  # Red for low confidence
                    
                    # Apply style to the primary code and confidence columns
                    for col in ['primary_code', 'primary_confidence']:
                        if col in row.index:
                            col_idx = row.index.get_loc(col)
                            styles[col_idx] = color
            return styles
        
        # Apply styling
        styled_df = preview_df.style.apply(highlight_confidence, axis=1)
        st.dataframe(styled_df)
    else:
        # Display without styling
        st.dataframe(preview_df)


def main():
    """Main Streamlit app function."""
    # Set page title and icon
    st.set_page_config(page_title="Dialog Coder", layout="wide")
    
    # App header
    st.title("Dialog Coder")
    st.markdown("Upload transcript and dictionary files to classify dialog content.")
    
    # File uploaders side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transcript File")
        transcript_file = st.file_uploader(
            "Upload transcript CSV or Excel file", 
            type=['csv', 'xlsx', 'xls'],
            help="File should contain dialog text in a 'text' column"
        )
        
    with col2:
        st.subheader("Dictionary File")
        dictionary_file = st.file_uploader(
            "Upload dictionary CSV or Excel file", 
            type=['csv', 'xlsx', 'xls'],
            help="File should contain keywords and codes to match"
        )
    
    # Load data when files are uploaded
    transcript_df = None
    dictionary_df = None
    
    if transcript_file:
        transcript_df = load_file(transcript_file)
        if transcript_df is not None:
            st.success(f"Loaded transcript with {len(transcript_df)} rows")
    
    if dictionary_file:
        dictionary_df = load_file(dictionary_file)
        if dictionary_df is not None:
            st.success(f"Loaded dictionary with {len(dictionary_df)} entries")
    
    # Column mapper expander
    if transcript_df is not None or dictionary_df is not None:
        with st.expander("Column Mapping", expanded=False):
            if transcript_df is not None:
                st.subheader("Transcript Preview")
                st.dataframe(transcript_df.head())
                
                # Text column selection
                text_col_options = list(transcript_df.columns)
                default_text_col = 'text'
                if default_text_col not in text_col_options:
                    for col in ['content', 'transcript', 'dialogue', 'utterance', 'message']:
                        if col in text_col_options:
                            default_text_col = col
                            break
                    else:
                        default_text_col = text_col_options[0] if text_col_options else None
                
                selected_text_col = st.selectbox(
                    "Select text column", 
                    options=text_col_options,
                    index=text_col_options.index(default_text_col) if default_text_col in text_col_options else 0,
                    key="text_col"
                )
                
                # If there's a temporary column rename required
                if selected_text_col != 'text' and selected_text_col is not None:
                    st.info(f"Will use '{selected_text_col}' as the text column")
                    transcript_df = transcript_df.rename(columns={selected_text_col: 'text'})
            
            if dictionary_df is not None:
                st.subheader("Dictionary Preview")
                st.dataframe(dictionary_df.head())
    
    # Confidence threshold slider
    threshold = st.slider(
        "Confidence Threshold", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.5, 
        step=0.05,
        help="Minimum confidence level required for classification"
    )
    
    # Classification button
    run_button = st.button("Run Classification", type="primary", disabled=(transcript_df is None or dictionary_df is None))
    
    # Results section
    if run_button and transcript_df is not None and dictionary_df is not None:
        try:
            with st.spinner("Running classification..."):
                # Save temporary files for processing
                temp_transcript_path = Path(os.path.join(os.path.dirname(__file__), 'temp_transcript.csv'))
                temp_dict_path = Path(os.path.join(os.path.dirname(__file__), 'temp_dict.csv'))
                
                transcript_df.to_csv(temp_transcript_path, index=False)
                dictionary_df.to_csv(temp_dict_path, index=False)
                
                # Run classification
                results_df = run_classification(
                    str(temp_transcript_path),
                    str(temp_dict_path),
                    threshold
                )
                
                # Clean up temp files
                try:
                    temp_transcript_path.unlink(missing_ok=True)
                    temp_dict_path.unlink(missing_ok=True)
                except Exception as e:
                    logger.log_warning(f"Error cleaning up temporary files: {str(e)}")
                
                # Show results
                st.subheader("Classification Results")
                st.write(f"Classified {len(results_df)} rows")
                
                # Show preview with color coding
                show_dataframe_preview(results_df)
                
                # Export results to CSV and create download button
                try:
                    output_path = export_csv(results_df, transcript_file.name)
                    
                    with open(output_path, 'rb') as file:
                        st.download_button(
                            label="Download Results CSV",
                            data=file,
                            file_name=output_path.name,
                            mime="text/csv",
                            help="Download the classified data as a CSV file"
                        )
                except Exception as e:
                    st.error(f"Error creating download file: {str(e)}")
                    logger.log_error("Error in file export", error=e)
                
        except Exception as e:
            st.error(f"Error during classification: {str(e)}")
            logger.log_error("Error in classification process", error=e)
    
    # Display footer
    st.markdown("---")
    st.caption("Dialog Coder - Plan B Classification System")


if __name__ == "__main__":
    main() 