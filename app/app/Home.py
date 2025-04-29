import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Transcript Coder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
with st.sidebar:
    st.page_link("Home.py", label="🏠 Home")
    st.page_link("pages/Dictionary.py", label="📚 Dictionary")
    st.page_link("pages/Upload.py", label="📤 Upload")
    st.page_link("pages/Reports.py", label="📊 Reports")

# Main page content
st.title("🎯 Welcome to Transcript Coder")

st.markdown("""
Effortlessly upload, code, and analyze your transcripts with ease.  
""")

st.divider()

st.subheader("🚀 Get Started")
st.markdown("""
- **Dictionary**: View or update the coding dictionary.
- **Upload**: Import your transcript CSV files.
- **Reports**: Analyze your coded transcripts and download reports.
""")

st.divider()

st.caption("Built with ❤️ using Streamlit | CITS5206 Group 3")
