import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# -----------------------------
# Load Environment Variables
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    PROJECT_ROOT / ".env"
)


API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


# -----------------------------
# Page Title
# -----------------------------

st.title(
    "LedgerLens Analytics"
)


# -----------------------------
# Load Prometheus Metrics
# -----------------------------

try:

    response = requests.get(
        f"{API_URL}/metrics",
        timeout=5
    )


    if response.status_code != 200:

        st.error(
            "Unable to load metrics from backend"
        )

        st.stop()


    metrics_text = response.text


except requests.exceptions.ConnectionError:

    st.error(
        "Backend is not running. "
        "Start FastAPI first."
    )

    st.stop()


except requests.exceptions.Timeout:

    st.error(
        "Backend request timed out."
    )

    st.stop()


except Exception as e:

    st.error(
        f"Metrics connection failed: {str(e)}"
    )

    st.stop()


# -----------------------------
# Prometheus Metrics
# -----------------------------

st.subheader(
    "System Metrics"
)


st.text_area(
    "Prometheus Metrics",
    metrics_text,
    height=300
)


# -----------------------------
# Invoice Statistics
# -----------------------------

st.subheader(
    "Invoice Overview"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Invoices Processed",
        "Coming soon"
    )


with col2:

    st.metric(
        "Auto Approved",
        "Coming soon"
    )


with col3:

    st.metric(
        "Average Confidence",
        "Coming soon"
    )


with col4:

    st.metric(
        "Pending Review",
        "Coming soon"
    )


# -----------------------------
# Processing Performance
# -----------------------------

st.subheader(
    "Processing Performance"
)


processing_time = {

    "Seconds": [
        3.2,
        3.5,
        3.1,
        2.9,
    ]

}


st.line_chart(
    processing_time
)