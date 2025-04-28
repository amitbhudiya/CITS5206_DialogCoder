import streamlit as st

st.title("📄 Upload Transcripts")

st.write("Upload your transcript CSV files here to start coding.")

uploaded_files = st.file_uploader(
    "Choose one or more transcript CSV files",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Uploaded {len(uploaded_files)} file(s)!")
    # (Later: Add processing logic here.)
else:
    st.info("Awaiting transcript uploads...")
