import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="Manage Coding Dictionary", layout="wide")

# Sidebar links
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

# Upload section
uploaded_file = st.file_uploader("🔼 Upload a new dictionary CSV", type="csv")

with st.expander("📋 View file format requirements"):
    st.markdown("""
    **Expected CSV Format:**
    - Columns: `category`, `keywords` (case-insensitive)
    - `keywords` should be a comma-separated list like `hello,hi,roger`
    - Example:
      ```
      category,keywords
      acknowledge,hello,hi,roger
      question,what,why,how
      ```
    """)

# Handle upload
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.lower() for col in df.columns]

        if set(df.columns) == REQUIRED_COLUMNS:
            # Backup old dictionary
            if os.path.exists(DICT_PATH):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(UPLOAD_FOLDER, f"dictionary_backup_{timestamp}.csv")
                os.rename(DICT_PATH, backup_path)

            df.to_csv(DICT_PATH, index=False)
            st.success("✅ Dictionary uploaded and saved successfully!")

        else:
            st.error(f"❌ CSV must have exactly these columns: {REQUIRED_COLUMNS}")
    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {e}")

# Load existing dictionary
if os.path.exists(DICT_PATH):
    st.subheader("📝 Current Dictionary")

    df = pd.read_csv(DICT_PATH)
    df.columns = [col.lower() for col in df.columns]

    # 🔍 Search/filter
    search_term = st.text_input("🔍 Search categories").lower()
    filtered_df = df[df['category'].str.lower().str.contains(search_term)] if search_term else df

    # ➕ Add new row
    if st.button("➕ Add Empty Row"):
        empty_row = pd.DataFrame([{"category": "", "keywords": ""}])
        filtered_df = pd.concat([filtered_df, empty_row], ignore_index=True)

    # 🧾 Show editable table
    edited_df = st.data_editor(
        filtered_df,
        num_rows="dynamic",
        use_container_width=True,
        key="dict_editor"
    )

    # 🧪 Basic validation
    if edited_df['category'].isnull().any() or edited_df['keywords'].isnull().any():
        st.warning("⚠️ Some rows have empty values.")
    elif edited_df['category'].duplicated().any():
        st.warning("⚠️ Duplicate category entries found.")

    # 💾 Save changes
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save Changes"):
            edited_df.to_csv(DICT_PATH, index=False)
            st.success("✅ Changes saved!")

    # 📥 Download
    with col2:
        csv_data = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", data=csv_data, file_name="dictionary.csv", mime="text/csv")

    # 📊 Stats
    st.markdown("---")
    st.metric("Total Entries", len(edited_df))
    st.metric("Unique Categories", edited_df['category'].nunique())
else:
    st.warning("⚠️ No dictionary uploaded yet.")
