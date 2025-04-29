import streamlit as st
st.set_page_config(page_title="Reports and Analysis", layout="wide")

# Sidebar navigation
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
st.sidebar.page_link("pages/Reports.py", label="📊 Reports")

st.title("📊 Reports and Analysis")

st.write("View coded results, summaries, and download reports here.")

# (Later: Add report charts, frequency tables here.)
st.info("Reports will appear here after processing transcripts.")
