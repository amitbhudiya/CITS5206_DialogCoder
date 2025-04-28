import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file_processor import process_uploaded_csv

import streamlit as st
import pandas as pd

def get_output_filename(input_filename):
    name, ext = os.path.splitext(input_filename)
    return f"{name}_coded{ext}"

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

    # Step 1: Upload
    st.markdown(
        """
        <div style='background-color:#e9f0fa;padding:18px 18px 8px 18px;border-radius:10px;margin-bottom:12px;border:1px solid #b6c8e6;'>
            <h4 style='margin-bottom:0;color:#222;'><b>📤 Step 1: Select File(s)</b></h4>
            <p style='color:#222;margin-top:4px;'>You can upload one or more CSV files. Each file must contain a <b>'text'</b> column.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="Each file must contain a 'text' column."
    )

    if uploaded_files:
        # Step 2: Processing
        st.markdown(
            """
            <div style='background-color:#f3f3f3;padding:14px 18px 8px 18px;border-radius:10px;margin-bottom:12px;border:1px solid #e0e0e0;'>
            <h4 style='margin-bottom:0;color:#222;'><b>⚙️ Step 2: Processing Progress</b></h4>
            <p style='color:#222;margin-top:4px;'>Your files are being processed. Please wait...</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        upload_dir = "./uploaded"
        output_dir = "./processed"
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_paths = []
        output_paths = []

        with st.spinner("Processing files, please wait..."):
            for uploaded_file in uploaded_files:
                input_path = os.path.join(upload_dir, uploaded_file.name)
                output_filename = get_output_filename(uploaded_file.name)
                output_path = os.path.join(output_dir, output_filename)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                input_paths.append(input_path)
                output_paths.append(output_path)

            if len(input_paths) == 1:
                process_uploaded_csv(input_paths[0], output_paths[0])
                st.success(f"✅ Processed file: {os.path.basename(output_paths[0])}")
            else:
                process_uploaded_csv(input_paths, output_paths)
                st.success(f"✅ Processed {len(uploaded_files)} files. Results are saved.")

        # Step 3: Results & Preview
        st.markdown(
            """
            <div style='background-color:#e0f7ea;padding:14px 18px 8px 18px;border-radius:10px;margin-bottom:12px;border:1px solid #7ed6a7;'>
            <h4 style='margin-bottom:0;color:#222;'><b>📊 Step 3: Download Results & Preview</b></h4>
            <p style='color:#222;margin-top:4px;'>Preview the results below. Click 'Show more' to expand, or download the full file.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        DEFAULT_PREVIEW_ROWS = 10
        EXPANDED_PREVIEW_ROWS = 50

        for idx, output_path in enumerate(output_paths):
            with st.container():
                try:
                    df_preview = pd.read_csv(output_path)
                    file_key = f"preview_expanded_{os.path.basename(output_path)}"
                    if file_key not in st.session_state:
                        st.session_state[file_key] = False

                    st.markdown(
                        f"""
                        <div style='background-color:#fff;border:1.5px solid #e0e7ef;padding:10px 10px 5px 10px;border-radius:8px;margin-bottom:8px;'>
                        <b style='color:#222;'>Preview of <span style='color:#4F8BF9'>{os.path.basename(output_path)}</span>:</b>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.session_state[file_key]:
                        st.dataframe(df_preview.head(EXPANDED_PREVIEW_ROWS), use_container_width=True)
                        if df_preview.shape[0] > EXPANDED_PREVIEW_ROWS:
                            if st.button("Show less", key=f"less_{idx}"):
                                st.session_state[file_key] = False
                    else:
                        st.dataframe(df_preview.head(DEFAULT_PREVIEW_ROWS), use_container_width=True)
                        if df_preview.shape[0] > DEFAULT_PREVIEW_ROWS:
                            if st.button("Show more", key=f"more_{idx}"):
                                st.session_state[file_key] = True
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Could not preview {os.path.basename(output_path)}: {e}")
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
