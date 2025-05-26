import streamlit as st
import os
import sys
import tempfile
import pandas as pd
from components.footer import show_footer
from components.sidebar import show_sidebar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from file_processor import process_multi_files, process_single_file


st.set_page_config(page_title="Upload Transcripts", layout="wide")

show_sidebar()
for key in [
    "uploaded_files",
    "processed_files",
    "temp_input_paths",
    "temp_output_paths",
    "processed_dfs",
]:
    if key not in st.session_state:
        st.session_state[key] = []

st.title("📄 Upload Transcripts")
st.markdown(
    ":sparkles: Upload your transcript CSV files here for automatic coding and analysis. :sparkles:"
)
DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), '../uploaded_dictionaries/dictionary.csv')
if not os.path.exists(DICTIONARY_PATH):
    st.warning("⚠️No dictionary found. Please upload or create new dictionary before processing the transcript.")
REPORT_FOLDER = os.path.join(os.path.dirname(__file__), '../uploaded_reports')
os.makedirs(REPORT_FOLDER, exist_ok=True)

with st.expander("📋 View file format requirements"):
    st.warning(
        """
            **⚠️ Important File Requirements:**
            - Only `.csv` files are supported
            - The file must contain a `text` column (case-insensitive)
            - Each row should contain one transcript entry
            - Plain text files will be auto-converted to CSV
        """
    )

st.subheader("⬆️ Upload Files:")
uploaded_files = st.file_uploader(
    "Upload one or more transcript CSV files",
    type="csv",
    accept_multiple_files=True,
    key="uploader",
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.temp_input_paths.clear()
    st.session_state.temp_output_paths.clear()
    st.session_state.processed_dfs.clear()

    # Process files without showing the upload list
    for file in uploaded_files:
        try:
            content = file.getvalue().decode("utf-8")
            if not content.strip():
                st.error(f"❌ File {file.name} is empty.")
                continue

            try:
                file.seek(0)
                df = pd.read_csv(file)
            except pd.errors.ParserError:
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                df = pd.DataFrame({"text": lines})

            if "text" not in df.columns and "Text" not in df.columns:
                if len(df.columns) == 1:
                    df.columns = ["text"]
                else:
                    st.error(
                        f"❌ File {file.name} does not contain a valid 'text' column."
                    )
                    continue

            temp_input = tempfile.NamedTemporaryFile(
                delete=False, suffix=".csv", prefix="dialogcoder_input_"
            )
            df.to_csv(temp_input.name, index=False)
            st.session_state.temp_input_paths.append(temp_input.name)

            temp_output = tempfile.NamedTemporaryFile(
                delete=False, suffix=".csv", prefix="dialogcoder_output_"
            )
            st.session_state.temp_output_paths.append(temp_output.name)

        except Exception as e:
            st.error(f"❌ Failed to process `{file.name}`: {e}")

    if len(st.session_state.temp_input_paths) == 1:
        process_single_file(
            st.session_state.temp_input_paths[0], st.session_state.temp_output_paths[0]
        )
    elif len(st.session_state.temp_input_paths) > 1:
        process_multi_files(
            st.session_state.temp_input_paths, st.session_state.temp_output_paths
        )

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
                mime="text/csv",

                key=f"download_processed_{idx}_{file.name}"

            )

        try:
            df = pd.read_csv(path)
            st.session_state["processed_dfs"].append(df)
        except Exception:
            st.error(f"❌ Failed to preview `{file.name}`.")

    # Display processed results
    if st.session_state["processed_dfs"]:
        # Display preview and frequency statistics for each file
        for idx, df in enumerate(st.session_state["processed_dfs"]):
            file_name = st.session_state["uploaded_files"][idx].name

            # Display file preview
            with st.expander(f"📄 Preview of `{file_name}`", expanded=True):
                st.dataframe(df, use_container_width=True, hide_index=True)

            # Display frequency statistics
            with st.expander(
                f"📊 B5T Code Frequency Statistics - {file_name}", expanded=True
            ):
                if "B5T" in df.columns:
                    freq_df = df["B5T"].value_counts().reset_index()
                    freq_df.columns = ["B5T", "Frequency"]
                    if not freq_df.empty and "B5T" in freq_df.columns:
                        freq_df["B5T"] = freq_df["B5T"].astype(str)
                        freq_df = freq_df.sort_values("B5T")
                        csv = freq_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            f"⬇️ Download B5T_frequency_{file_name}",
                            csv,
                            file_name=f"B5T_frequency_{file_name}",
                            mime="text/csv",

                            key=f"download_frequency_{idx}_{file_name}"

                        )
                        st.dataframe(freq_df, use_container_width=True)
                    else:
                        st.warning(f"⚠️ No valid B5T codes found in {file_name}.")
                else:
                    st.warning(
                        f"⚠️ No 'B5T' column found in {file_name}. Cannot generate summary."
                    )

        # Display combined statistics
        with st.expander("📊 Combined B5T Code Frequency Statistics", expanded=True):
            combined_df = pd.concat(
                st.session_state["processed_dfs"], ignore_index=True
            )
            if "B5T" in combined_df.columns:
                freq_df = combined_df["B5T"].value_counts().reset_index()
                freq_df.columns = ["B5T", "Frequency"]
                if not freq_df.empty and "B5T" in freq_df.columns:
                    freq_df["B5T"] = freq_df["B5T"].astype(str)
                    freq_df = freq_df.sort_values("B5T")
                    csv = freq_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Download Combined_B5T_frequency.csv",
                        csv,
                        file_name="Combined_B5T_frequency.csv",
                        mime="text/csv",

                        key="download_combined_frequency"

                    )
                    st.dataframe(freq_df, use_container_width=True)
                else:
                    st.warning("⚠️ No valid B5T codes found in combined data.")
            else:
                st.warning(
                    "⚠️ No 'B5T' column found in any processed data. Cannot generate combined summary."
                )

# Display cached results when returning from other pages
elif st.session_state["uploaded_files"]:
    st.success("Showing previously uploaded transcripts (cached).")

    # Display preview and frequency statistics for each file
    for i, df in enumerate(st.session_state["processed_dfs"]):
        fname = st.session_state["uploaded_files"][i].name

        # Display file preview
        with st.expander(f"📄 Preview of `{fname}`", expanded=True):
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Display frequency statistics
        with st.expander(f"📊 B5T Code Frequency Statistics - {fname}", expanded=True):
            if "B5T" in df.columns:
                freq_df = df["B5T"].value_counts().reset_index()
                freq_df.columns = ["B5T", "Frequency"]
                if not freq_df.empty and "B5T" in freq_df.columns:
                    freq_df["B5T"] = freq_df["B5T"].astype(str)
                    freq_df = freq_df.sort_values("B5T")
                    csv = freq_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        f"⬇️ Download B5T_frequency_{fname}",
                        csv,
                        file_name=f"B5T_frequency_{fname}",
                        mime="text/csv",

                        key=f"download_frequency_cached_{i}_{fname}"

                    )
                    st.dataframe(freq_df, use_container_width=True)
                else:
                    st.warning(f"⚠️ No valid B5T codes found in {fname}.")
            else:
                st.warning(
                    f"⚠️ No 'B5T' column found in {fname}. Cannot generate summary."
                )

    # Display combined statistics
    with st.expander("📊 Combined B5T Code Frequency Statistics", expanded=True):
        combined_df = pd.concat(st.session_state["processed_dfs"], ignore_index=True)
        if "B5T" in combined_df.columns:
            freq_df = combined_df["B5T"].value_counts().reset_index()
            freq_df.columns = ["B5T", "Frequency"]
            if not freq_df.empty and "B5T" in freq_df.columns:
                freq_df["B5T"] = freq_df["B5T"].astype(str)
                freq_df = freq_df.sort_values("B5T")
                csv = freq_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Combined_B5T_frequency.csv",
                    csv,
                    file_name="Combined_B5T_frequency.csv",
                    mime="text/csv",

                    key="download_combined_frequency_cached"

                )
                st.dataframe(freq_df, use_container_width=True)
            else:
                st.warning("⚠️ No valid B5T codes found in combined data.")
        else:
            st.warning(
                "⚠️ No 'B5T' column found in any processed data. Cannot generate combined summary."
            )

else:
    st.info("Upload transcript CSV files to begin.")

# Display footer
show_footer()
