import streamlit as st
st.set_page_config(page_title="Manage Coding Dictionary", layout="wide")
import pandas as pd
import os

# Sidebar navigation
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
st.sidebar.page_link("pages/Reports.py", label="📊 Reports")

st.title("📚 Manage Coding Dictionary")

# Setup dictionary saving
UPLOAD_FOLDER = "uploaded_dictionaries"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DICT_PATH = os.path.join(UPLOAD_FOLDER, "dictionary.csv")
REQUIRED_COLUMNS = {"category", "keywords"}

uploaded_file = st.file_uploader("Upload a new dictionary CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if set(df.columns.str.lower()) == REQUIRED_COLUMNS:
        df.to_csv(DICT_PATH, index=False)
        st.success("✅ Dictionary uploaded and saved!")
    else:
        st.error(f"❌ CSV must have exactly these columns: {REQUIRED_COLUMNS}")

if os.path.exists(DICT_PATH):
    st.subheader("📚 Current Dictionary")
    existing_df = pd.read_csv(DICT_PATH)
    edited_df = st.data_editor(existing_df, num_rows="dynamic", use_container_width=True)
    if st.button("💾 Save Changes"):
        edited_df.to_csv(DICT_PATH, index=False)
        st.success("Changes saved successfully!")
else:
    st.warning("No dictionary uploaded yet.")
