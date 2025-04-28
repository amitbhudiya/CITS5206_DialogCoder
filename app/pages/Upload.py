import streamlit as st
st.set_page_config(page_title="Upload Transcripts", layout="wide")
import pandas as pd
import tempfile
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from file_processor import process_single_file, process_uploaded_csv

st.title("📄 Upload Transcripts")
st.markdown(":sparkles: Upload your transcript CSV files here for automatic coding and analysis. :sparkles:")
st.divider()

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
                # Save uploaded file to temporary directory
                temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                df.to_csv(temp_input.name, index=False)
                temp_input_paths.append(temp_input.name)
                # Pre-generate output file path
                temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                temp_output_paths.append(temp_output.name)
            except Exception as e:
                st.error(f"❌ Preview failed: {e}")
        # Process and generate downloadable files
        if len(temp_input_paths) == 1:
            process_single_file(temp_input_paths[0], temp_output_paths[0])
        elif len(temp_input_paths) > 1:
            process_uploaded_csv(temp_input_paths, temp_output_paths)
        # Download button and result preview
        for idx, file in enumerate(uploaded_files):
            with open(temp_output_paths[idx], "rb") as f:
                st.download_button(
                    label=f"⬇️ Download processed result: processed_{file.name}",
                    data=f.read(),
                    file_name=f"processed_{file.name}",
                    mime="text/csv"
                )
            # Result preview (Show more button)
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
                            pass  # Low version compatibility, no error but will not auto refresh
            except Exception as e:
                st.error(f"❌ Result preview failed: {e}")
    else:
        st.info("Please upload transcript CSV files. Batch upload is supported.")

st.markdown('<hr style="border: 0; height: 3px; background: linear-gradient(90deg, #36d1c4, #5b86e5, #f7971e);">', unsafe_allow_html=True)
st.caption("For any questions, please contact the administrator | Built with ❤️ using Streamlit")
