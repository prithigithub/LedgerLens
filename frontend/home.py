import streamlit as st


st.set_page_config(
    page_title="LedgerLens",
    page_icon="📄",
    layout="wide",
)


st.title("📄 LedgerLens")


st.subheader(
    "AI-Powered Intelligent Invoice Processing Platform"
)


st.write(
    """
LedgerLens uses multimodal AI to:

- Extract invoice information
- Validate results
- Score confidence
- Route uncertain fields for human review
- Maintain audit history
"""
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "AI Model",
        "GPT-4o Vision",
    )


with col2:
    st.metric(
        "Validation",
        "Pydantic",
    )


with col3:
    st.metric(
        "Workflow",
        "Human + AI",
    )