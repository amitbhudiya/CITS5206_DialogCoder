import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reports and Analysis", layout="wide")

# Sidebar navigation
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
st.sidebar.page_link("pages/Reports.py", label="📊 Reports")

st.title("📊 Reports and Analysis")

REPORT_FOLDER = "uploaded_reports"

if os.path.exists(REPORT_FOLDER):
    # Summary frequency report
    summary_path = os.path.join(REPORT_FOLDER, "summary_frequency.csv")
    if os.path.exists(summary_path):
        st.header("📈 Summary Frequency Report")
        freq_df = pd.read_csv(summary_path)
        st.dataframe(freq_df, use_container_width=True)
        st.bar_chart(freq_df.set_index("code"))
        with open(summary_path, "rb") as f:
            st.download_button("⬇️ Download Summary Frequency CSV", data=f, file_name="summary_frequency.csv", mime="text/csv")
    else:
        st.warning("Summary frequency report not found. Please upload and process transcripts first.")

    st.divider()
    st.header("📄 Individual Processed Files")
    processed_files = [f for f in os.listdir(REPORT_FOLDER) if f.startswith("processed_")]
    if processed_files:
        for pfile in processed_files:
            st.write(f"📄 {pfile}")
            ppath = os.path.join(REPORT_FOLDER, pfile)
            df = pd.read_csv(ppath)
            st.dataframe(df.head(), use_container_width=True)
            with open(ppath, "rb") as f:
                st.download_button(f"⬇️ Download {pfile}", data=f, file_name=pfile, mime="text/csv")
    else:
        st.info("No processed individual files available.")
else:
    st.info("No reports generated yet. Please upload and process transcripts first.")
