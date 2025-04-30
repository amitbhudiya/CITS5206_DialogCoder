import streamlit as st
st.set_page_config(page_title="Upload Transcripts", layout="wide")

from components.sidebar import show_sidebar
show_sidebar()

import pandas as pd
import tempfile
import os
import sys
import shutil
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from file_processor import process_single_file, process_uploaded_csv

# Initialize session_state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []
if 'temp_input_paths' not in st.session_state:
    st.session_state.temp_input_paths = []
if 'temp_output_paths' not in st.session_state:
    st.session_state.temp_output_paths = []

st.title("📄 Upload Transcripts")
st.markdown(":sparkles: Upload your transcript CSV files here for automatic coding and analysis. :sparkles:")
st.divider()

REPORT_FOLDER = "uploaded_reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

with st.container():
    with st.expander("📋 View file format requirements"):
        st.markdown("""
        - Only `.csv` files are supported
        - The file must contain a `text` column (case-insensitive)
        - It is recommended that each row contains one transcript entry
        - If the file is a simple text file with one entry per line, it will be automatically converted to CSV format
        """)
    st.subheader("⬆️ Upload Files:")
    uploaded_files = st.file_uploader(
        "Select one or more transcript CSV files to upload",
        type="csv",
        accept_multiple_files=True,
        key="uploader"
    )

    # Update file list in session_state
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"Successfully uploaded {len(uploaded_files)} file(s)!")
        
        # Clear previous temporary file paths
        st.session_state.temp_input_paths = []
        st.session_state.temp_output_paths = []
        
        for file in uploaded_files:
            st.write(f"- :page_facing_up: `{file.name}`")
            try:
                # Check if file is empty
                file_content = file.getvalue().decode('utf-8')
                if not file_content.strip():
                    st.error(f"❌ File {file.name} is empty")
                    continue
                
                # Try to read CSV file
                try:
                    # Reset file pointer
                    file.seek(0)
                    df = pd.read_csv(file)
                except pd.errors.EmptyDataError:
                    # Skip if file is empty
                    st.error(f"❌ File {file.name} is empty")
                    continue
                except pd.errors.ParserError:
                    # If not standard CSV format, treat as text file
                    lines = [line.strip() for line in file_content.split('\n') if line.strip()]
                    df = pd.DataFrame({'text': lines})
                
                # Check if required columns exist
                if 'text' not in df.columns and 'Text' not in df.columns:
                    # If first row is header, try to use it as column names
                    if len(df.columns) == 1:
                        df.columns = ['text']
                    else:
                        st.error(f"❌ File {file.name} does not contain a 'text' column")
                        continue
                
                temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                df.to_csv(temp_input.name, index=False)
                st.session_state.temp_input_paths.append(temp_input.name)
                temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                st.session_state.temp_output_paths.append(temp_output.name)
            except Exception as e:
                st.error(f"❌ Preview failed for {file.name}: {str(e)}")

        if len(st.session_state.temp_input_paths) == 1:
            process_single_file(st.session_state.temp_input_paths[0], st.session_state.temp_output_paths[0])
        elif len(st.session_state.temp_input_paths) > 1:
            process_uploaded_csv(st.session_state.temp_input_paths, st.session_state.temp_output_paths)

    # Display uploaded files (if any)
    if st.session_state.uploaded_files:
        st.write("**Uploaded files and preview:**")
        for file in st.session_state.uploaded_files:
            st.write(f"- :page_facing_up: `{file.name}`")
            try:
                # Check if file is empty
                file_content = file.getvalue().decode('utf-8')
                if not file_content.strip():
                    st.error(f"❌ File {file.name} is empty")
                    continue
                
                # Try to read CSV file
                try:
                    # Reset file pointer
                    file.seek(0)
                    df = pd.read_csv(file)
                except pd.errors.EmptyDataError:
                    # Skip if file is empty
                    st.error(f"❌ File {file.name} is empty")
                    continue
                except pd.errors.ParserError:
                    # If not standard CSV format, treat as text file
                    lines = [line.strip() for line in file_content.split('\n') if line.strip()]
                    df = pd.DataFrame({'text': lines})
                
                # Check if required columns exist
                if 'text' not in df.columns and 'Text' not in df.columns:
                    # If first row is header, try to use it as column names
                    if len(df.columns) == 1:
                        df.columns = ['text']
                    else:
                        st.error(f"❌ File {file.name} does not contain a 'text' column")
                        continue
                
                st.dataframe(df.head(), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"❌ Preview failed for {file.name}: {str(e)}")

        all_results = []
        # Clear old reports with user confirmation
        if st.button("Clear old reports in the folder?"):
            for old_file in os.listdir(REPORT_FOLDER):
                try:
                    os.remove(os.path.join(REPORT_FOLDER, old_file))
                except OSError as e:
                    st.warning(f"⚠️ Could not delete file {old_file}: {e}")

        for idx, file in enumerate(st.session_state.uploaded_files):
            try:
                with open(st.session_state.temp_output_paths[idx], "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download processed result: processed_{file.name}",
                        data=f.read(),
                        file_name=f"processed_{file.name}",
                        mime="text/csv"
                    )
                result_df = pd.read_csv(st.session_state.temp_output_paths[idx])
                show_rows_key = f"show_rows_{idx}"
                if show_rows_key not in st.session_state:
                    st.session_state[show_rows_key] = 5
                st.markdown(f"**Processed result preview:** :eyes:")
                st.dataframe(result_df.head(st.session_state[show_rows_key]), use_container_width=True, hide_index=True)
                if st.session_state[show_rows_key] < len(result_df):
                    if st.button(f"Show more ({file.name})", key=f"show_more_{idx}"):
                        st.session_state[show_rows_key] = min(st.session_state[show_rows_key] + 10, len(result_df))
                        try:
                            st.experimental_rerun()
                        except AttributeError:
                            pass
                all_results.append(result_df)
            except Exception as e:
                st.error(f"❌ Result preview failed for {file.name}: {str(e)}")

        if all_results:
            combined_df = pd.concat(all_results, ignore_index=True)
            st.write("Processed data columns:", combined_df.columns.tolist())  # Display all column names
            if "B5T" in combined_df.columns:
                freq_df = combined_df["B5T"].value_counts().reset_index()
                freq_df.columns = ["code", "frequency"]
                freq_df = freq_df.sort_values("code")
                freq_df.to_csv(os.path.join(REPORT_FOLDER, "summary_frequency.csv"), index=False)
                st.success("✅ Successfully generated code frequency summary file!")
            else:
                st.warning("⚠️ No 'B5T' column found in processed data, cannot generate frequency summary.")

            for idx, file in enumerate(st.session_state.uploaded_files):
                try:
                    shutil.copy(st.session_state.temp_output_paths[idx], os.path.join(REPORT_FOLDER, f"processed_{file.name}"))
                except Exception as e:
                    st.error(f"❌ Failed to save processed file {file.name}: {str(e)}")

    else:
        st.info("Please upload transcript CSV files. Batch upload is supported.")

st.markdown('<hr style="border: 0; height: 3px; background: linear-gradient(90deg, #36d1c4, #5b86e5, #f7971e);">', unsafe_allow_html=True)
st.caption("For any questions, please contact the administrator | Built with ❤️ using Streamlit")
