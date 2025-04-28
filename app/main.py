import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file_processor import process_uploaded_csv

import streamlit as st

# Setup page config
st.set_page_config(page_title="Transcript Coder", layout="wide")

# --- Navigation Bar (Tabs) ---
tab_home, tab_upload, tab_dictionary, tab_reports = st.tabs(["🏠 Home", "📄 Upload", "📚 Dictionary", "📊 Reports"])

# --- Home Tab ---
with tab_home:
    st.title("🏠 Home")
    st.write("Welcome to the Transcript Coder App.")

# --- Upload Tab ---
with tab_upload:
    st.title("📄 Upload Transcript Files")
    st.markdown("Upload your transcript CSV files. The system will automatically process them in batch. Both single and multiple file uploads are supported.")

    st.markdown("---")

    with st.container():
        st.subheader("Step 1: Select File(s)")
        uploaded_files = st.file_uploader(
            "Please select one or more CSV files",
            type=["csv"],
            accept_multiple_files=True,
            help="Each file must contain a 'text' column."
        )

    if uploaded_files:
        st.markdown("---")
        st.subheader("Step 2: Processing Progress")
        upload_dir = "./uploaded"
        output_dir = "./processed"
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_paths = []
        output_paths = []

        with st.spinner("Processing files, please wait..."):
            for uploaded_file in uploaded_files:
                input_path = os.path.join(upload_dir, uploaded_file.name)
                output_path = os.path.join(output_dir, uploaded_file.name)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                input_paths.append(input_path)
                output_paths.append(output_path)

            # Single or multiple file processing
            if len(input_paths) == 1:
                process_uploaded_csv(input_paths[0], output_paths[0])
                st.success(f"✅ Processed file: {os.path.basename(output_paths[0])}")
            else:
                process_uploaded_csv(input_paths, output_paths)
                st.success(f"✅ Processed {len(uploaded_files)} files. Results are saved.")

        st.markdown("---")
        st.subheader("Step 3: Download Results")
        for output_path in output_paths:
            with open(output_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ Download {os.path.basename(output_path)}",
                    data=f,
                    file_name=os.path.basename(output_path),
                    mime="text/csv"
                )
    else:
        st.info("Please upload one or more CSV files first.")

# --- Dictionary Tab ---
with tab_dictionary:
    st.title("📚 Dictionary")
    st.write("Manage your coding dictionary here.")

# --- Reports Tab ---
with tab_reports:
    st.title("📊 Reports")
    st.write("View and export your analysis reports here.")
