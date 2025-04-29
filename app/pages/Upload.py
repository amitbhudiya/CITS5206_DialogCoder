import streamlit as st
st.set_page_config(page_title="Upload Transcripts", layout="wide")
import pandas as pd
import tempfile
import os
import sys
import shutil

# Sidebar navigation
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
st.sidebar.page_link("pages/Reports.py", label="📊 Reports")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from file_processor import process_single_file, process_uploaded_csv

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
        """)
    st.subheader("⬆️ Upload Files:")
    uploaded_files = st.file_uploader(
        "Select one or more transcript CSV files to upload",
        type="csv",
        accept_multiple_files=True,
        key="uploader"
    )

    if uploaded_files:
        st.success(f"Successfully uploaded {len(uploaded_files)} file(s)!")
        st.write("**Uploaded files and preview:**")
        temp_input_paths = []
        temp_output_paths = []
        for file in uploaded_files:
            st.write(f"- :page_facing_up: `{file.name}`")
            try:
                df = pd.read_csv(file)
                st.dataframe(df.head(), use_container_width=True, hide_index=True)
                temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                df.to_csv(temp_input.name, index=False)
                temp_input_paths.append(temp_input.name)
                temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                temp_output_paths.append(temp_output.name)
            except Exception as e:
                st.error(f"❌ Preview failed: {e}")

        if len(temp_input_paths) == 1:
            process_single_file(temp_input_paths[0], temp_output_paths[0])
        elif len(temp_input_paths) > 1:
            process_uploaded_csv(temp_input_paths, temp_output_paths)

        all_results = []
        # Clear old reports with user confirmation
        if st.button("Clear old reports in the folder?"):
            for old_file in os.listdir(REPORT_FOLDER):
                os.remove(os.path.join(REPORT_FOLDER, old_file))

        for idx, file in enumerate(uploaded_files):
            with open(temp_output_paths[idx], "rb") as f:
                st.download_button(
                    label=f"⬇️ Download processed result: processed_{file.name}",
                    data=f.read(),
                    file_name=f"processed_{file.name}",
                    mime="text/csv"
                )
            try:
                result_df = pd.read_csv(temp_output_paths[idx])
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
                st.error(f"❌ Result preview failed: {e}")

        if all_results:
            combined_df = pd.concat(all_results, ignore_index=True)
            if "code" in combined_df.columns:
                freq_df = combined_df["code"].value_counts().reset_index()
                freq_df.columns = ["code", "frequency"]
                freq_df = freq_df.sort_values("code")
                freq_df.to_csv(os.path.join(REPORT_FOLDER, "summary_frequency.csv"), index=False)

            for idx, file in enumerate(uploaded_files):
                shutil.copy(temp_output_paths[idx], os.path.join(REPORT_FOLDER, f"processed_{file.name}"))

    else:
        st.info("Please upload transcript CSV files. Batch upload is supported.")

st.markdown('<hr style="border: 0; height: 3px; background: linear-gradient(90deg, #36d1c4, #5b86e5, #f7971e);">', unsafe_allow_html=True)
st.caption("For any questions, please contact the administrator | Built with ❤️ using Streamlit")
