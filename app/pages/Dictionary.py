import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Manage Coding Dictionary", layout="wide")

# Sidebar links
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
st.sidebar.page_link("pages/Reports.py", label="📊 Reports")

# Title
st.title("📚 Manage Coding Dictionary")

# Directory and file setup
UPLOAD_FOLDER = "uploaded_dictionaries"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DICT_PATH = os.path.join(UPLOAD_FOLDER, "dictionary.csv")
REQUIRED_COLUMNS = {"category", "keywords"}

# Upload new dictionary
uploaded_file = st.file_uploader("🔼 Upload a new dictionary CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # Normalize columns
        df.columns = [col.lower() for col in df.columns]
        if set(df.columns) == REQUIRED_COLUMNS:
            df.to_csv(DICT_PATH, index=False)
            st.success("✅ Dictionary uploaded and saved successfully!")
        else:
            st.error(f"❌ CSV must have exactly these columns: {REQUIRED_COLUMNS}")
    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {e}")

# Display and edit existing dictionary
if os.path.exists(DICT_PATH):
    st.subheader("📝 Current Dictionary")
    existing_df = pd.read_csv(DICT_PATH)
    edited_df = st.data_editor(
        existing_df,
        num_rows="dynamic",
        use_container_width=True,
        key="dict_editor"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save Changes"):
            edited_df.to_csv(DICT_PATH, index=False)
            st.success("✅ Changes saved!")
    with col2:
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Dictionary CSV", data=csv, file_name="dictionary.csv", mime='text/csv')
else:
    st.warning("⚠️ No dictionary uploaded yet.")
