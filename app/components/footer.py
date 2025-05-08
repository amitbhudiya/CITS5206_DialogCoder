import streamlit as st


def show_footer():
    # Add CSS styles
    st.markdown(
        """
        <style>
        .footer {
            position: relative;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            text-align: center;
            padding: 10px;
            border-top: 1px solid rgba(230, 230, 230, 0.5);
            margin-top: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Add footer content
    st.markdown(
        """
        <div class="footer">
            <p style="color: gray; margin: 0;">Built with ❤️ using Streamlit | CITS5206 Group 3</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
