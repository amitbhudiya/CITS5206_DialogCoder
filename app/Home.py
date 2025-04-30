import streamlit as st
from components.sidebar import show_sidebar
from components.footer import show_footer

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Transcript Coder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show navigation bar
show_sidebar()

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

# Display footer
show_footer()