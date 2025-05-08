import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Reports and Analysis", layout="wide")

from components.footer import show_footer
from components.sidebar import show_sidebar

show_sidebar()

st.title("📊 Reports and Analysis")


def aggregate_frequencies(dfs):
    """Aggregate B5T frequencies from multiple DataFrames."""
    if not dfs:
        return None

    # Check if 'B5T' column exists in DataFrames
    valid_dfs = [df for df in dfs if "B5T" in df.columns]
    if not valid_dfs:
        return None

    # Combine DataFrames and calculate frequencies
    combined = pd.concat(valid_dfs, ignore_index=True)
    freq = combined["B5T"].value_counts().reset_index()
    freq.columns = ["B5T", "frequency"]
    return freq.sort_values("B5T")


# Access processed DataFrames from session_state
if "processed_dfs" in st.session_state and st.session_state["processed_dfs"]:
    processed_dfs = st.session_state["processed_dfs"]

    st.success(f"Found {len(processed_dfs)} processed transcript(s) for analysis.")

    # Show summary of each processed file
    with st.expander("📑 Processed Transcript Summaries", expanded=False):
        for i, df in enumerate(processed_dfs):
            st.subheader(f"Transcript #{i+1}")

            # Display basic statistics
            st.write(f"**Rows:** {len(df)}")
            st.write(f"**Columns:** {', '.join(df.columns)}")

            # Show preview of the data
            st.dataframe(df.head(), use_container_width=True, hide_index=True)

            # Show B5T distribution for this file
            if "B5T" in df.columns:
                file_freq = df["B5T"].value_counts().reset_index()
                file_freq.columns = ["B5T", "count"]
                st.caption("B5T distribution in this transcript:")
                st.dataframe(file_freq, use_container_width=True, hide_index=True)

            st.divider()

    # Calculate frequency table for all transcripts
    freq_df = aggregate_frequencies(processed_dfs)

    if freq_df is not None:
        st.header("🔍 Code Frequency Analysis")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Frequency Table")
            st.dataframe(freq_df, use_container_width=True, hide_index=True)

            # Download button for frequency table
            csv = freq_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Frequency Table CSV",
                data=csv,
                file_name="B5T_frequencies.csv",
                mime="text/csv",
            )

        with col2:
            st.subheader("Total Occurrences")
            st.metric("Total Coded Segments", freq_df["frequency"].sum())
            st.metric("Unique Codes", len(freq_df))

            # Show most frequent codes
            most_freq = freq_df.sort_values("frequency", ascending=False).head(3)
            st.caption("Top 3 most frequent codes:")
            for _, row in most_freq.iterrows():
                st.write(f"**{row['B5T']}**: {row['frequency']} occurrences")

        # Bar chart visualization
        st.subheader("📊 Visualization")
        st.bar_chart(freq_df.set_index("B5T"))

        # Pie chart option
        if st.checkbox("Show Pie Chart"):
            fig, ax = plt.subplots(figsize=(10, 10))
            freq_df.plot.pie(y="frequency", labels=freq_df["B5T"], ax=ax, legend=False)
            st.pyplot(fig)
    else:
        st.warning(
            "The processed transcripts do not contain 'B5T' column. Please ensure your transcripts were properly coded."
        )

else:
    st.info(
        "No processed transcripts available. Please upload and process transcripts first."
    )

# Display footer
show_footer()
