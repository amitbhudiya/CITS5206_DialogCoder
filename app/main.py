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
    st.title("📄 Upload")
    st.write("Upload your transcript files here.")

# --- Dictionary Tab ---
with tab_dictionary:
    st.title("📚 Dictionary")
    st.write("Manage your coding dictionary here.")

# --- Reports Tab ---
with tab_reports:
    st.title("📊 Reports")
    st.write("View and export your analysis reports here.")
