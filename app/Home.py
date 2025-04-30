import streamlit as st
from components.sidebar import show_sidebar

# Page configuration - 必须是第一个 Streamlit 命令
st.set_page_config(
    page_title="Transcript Coder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 显示导航栏
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

st.divider()

st.caption("Built with ❤️ using Streamlit | CITS5206 Group 3")
