# app/main.py

import streamlit as st

# Configure the base layout of the Streamlit app
# Sets page title and enables full-width layout
st.set_page_config(page_title="Transcript Coder", layout="wide")

# Sidebar setup: acts as the main navigation component
# Allows users to switch between core functional pages
st.sidebar.title("Transcript Coder")
page = st.sidebar.selectbox("Navigate to", ["Home", "Upload", "Dictionary", "Reports"])

# Display the page title at the top of the main view
st.title("Transcript Coder")

# Route logic — loads corresponding page content based on sidebar selection
# Each condition will later be replaced by a modular subcomponent or script
if page == "Home":
    st.write("Welcome to the Transcript Coder!")

elif page == "Upload":
    # TODO: Implement transcript file upload functionality
    st.write("Upload your transcript file here.")

elif page == "Dictionary":
    # TODO: Integrate dictionary management interface (import, edit, validate)
    st.write("Manage your coding dictionary.")

elif page == "Reports":
    # TODO: Add visualisations and exportable report generation
    st.write("View reports and analysis.")
