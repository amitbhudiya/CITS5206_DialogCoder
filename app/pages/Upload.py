import streamlit as st
st.set_page_config(page_title="Upload Transcripts", layout="wide")

import os
import tempfile
import sys
import pandas as pd

from components.sidebar import show_sidebar
show_sidebar()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from file_processor import process_single_file, process_uploaded_csv

for key in ['uploaded_files', 'processed_files', 'temp_input_paths', 'temp_output_paths', 'processed_dfs']:
    if key not in st.session_state:
        st.session_state[key] = []

st.title("📄 Upload Transcripts")
st.markdown(":sparkles: Upload your transcript CSV files here for automatic coding and analysis. :sparkles:")
st.divider()

REPORT_FOLDER = "uploaded_reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

with st.expander("📋 View file format requirements"):
    st.markdown("""
    - Only `.csv` files are supported  
    - The file must contain a `text` column (case-insensitive)  
    - Each row should contain one transcript entry  
    - Plain text files will be auto-converted to CSV  
    """)

st.subheader("⬆️ Upload Files:")
uploaded_files = st.file_uploader(
    "Upload one or more transcript CSV files",
    type="csv",
    accept_multiple_files=True,
    key="uploader"
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.temp_input_paths.clear()
    st.session_state.temp_output_paths.clear()
    st.session_state.processed_dfs.clear()

    for file in uploaded_files:
        st.write(f":page_facing_up: `{file.name}`")
        try:
            content = file.getvalue().decode("utf-8")
            if not content.strip():
                st.error(f"❌ File {file.name} is empty.")
                continue

            try:
                file.seek(0)
                df = pd.read_csv(file)
            except pd.errors.ParserError:
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                df = pd.DataFrame({'text': lines})

            if 'text' not in df.columns and 'Text' not in df.columns:
                if len(df.columns) == 1:
                    df.columns = ['text']
                else:
                    st.error(f"❌ File {file.name} does not contain a valid 'text' column.")
                    continue

            temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', prefix='dialogcoder_input_')
            df.to_csv(temp_input.name, index=False)
            st.session_state.temp_input_paths.append(temp_input.name)

            temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', prefix='dialogcoder_output_')
            st.session_state.temp_output_paths.append(temp_output.name)

        except Exception as e:
            st.error(f"❌ Failed to process `{file.name}`: {e}")

    if len(st.session_state.temp_input_paths) == 1:
        process_single_file(st.session_state.temp_input_paths[0], st.session_state.temp_output_paths[0])
    elif len(st.session_state.temp_input_paths) > 1:
        process_uploaded_csv(st.session_state.temp_input_paths, st.session_state.temp_output_paths)

    for idx, file in enumerate(st.session_state.uploaded_files):
        try:
            path = st.session_state.temp_output_paths[idx]
        except IndexError:
            st.warning(f"⚠️ Skipping `{file.name}`: no processed output found.")
            continue

        if not os.path.exists(path):
            st.warning(f"⚠️ Skipping `{file.name}`: processed file not found.")
            continue

        with open(path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download processed result: processed_{file.name}",
                data=f.read(),
                file_name=f"processed_{file.name}",
                mime="text/csv"
            )

        try:
            df = pd.read_csv(path)
            st.session_state['processed_dfs'].append(df)
            st.markdown(f"**Preview of `{file.name}`:**")
            st.dataframe(df.head(), use_container_width=True, hide_index=True)
        except Exception:
            st.error(f"❌ Failed to preview `{file.name}`.")

    if st.session_state['processed_dfs']:
        combined_df = pd.concat(st.session_state['processed_dfs'], ignore_index=True)
        st.markdown("### 📊 Summary Report (B5T frequency)")

        if "B5T" in combined_df.columns:
            freq_df = combined_df["B5T"].value_counts().reset_index()
            freq_df.columns = ["code", "frequency"]
            freq_df = freq_df.sort_values("code")

            csv = freq_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download summary_frequency.csv", csv, file_name="summary_frequency.csv", mime="text/csv")
            st.dataframe(freq_df, use_container_width=True)
        else:
            st.warning("⚠️ No 'B5T' column found in processed data. Cannot generate summary.")
else:
    st.info("Upload transcript CSV files to begin.")
