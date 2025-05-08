import streamlit as st


def show_sidebar():
    # Add CSS to hide default navigation bar and adjust button size
    st.markdown(
        """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        .stSidebar .stButton button {
            width: 100%;
            padding: 1rem 1.25rem;
            font-size: 1.3rem;
            margin: 0.75rem 0;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }
        .stSidebar .stButton button:hover {
            background-color: #f0f2f6;
            transform: scale(1.02);
        }
        /* Adjust icon size */
        .stSidebar .stButton button::before {
            font-size: 1.5rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    st.sidebar.page_link("Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/Dictionary.py", label="📚 Dictionary")
    st.sidebar.page_link("pages/Upload.py", label="📤 Upload")
    st.sidebar.page_link("pages/Reports.py", label="📊 Reports")
