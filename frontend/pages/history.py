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
    "http://backend:8000"
)


# -----------------------------
# Page Title
# -----------------------------

st.title(
    "Invoice History"
)


# -----------------------------
# Get Invoice History
# -----------------------------

try:

    response = requests.get(
        f"{API_URL}/documents/",
        timeout=5
    )


    if response.status_code != 200:

        st.error(
            "Unable to load invoice history."
        )

        st.stop()


    documents = response.json()


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
        f"Backend connection failed: {str(e)}"
    )

    st.stop()


# -----------------------------
# No Documents
# -----------------------------

if not documents:

    st.info(
        "No invoices processed yet."
    )


# -----------------------------
# Display Documents
# -----------------------------

else:

    st.write(
        f"Total Documents: {len(documents)}"
    )


    for doc in documents:

        st.divider()


        st.subheader(
            "Invoice: "
            f"{doc.get('filename', 'Unknown')}"
        )


        col1, col2, col3 = st.columns(3)


        # -----------------------------
        # Status
        # -----------------------------

        with col1:

            st.write(
                "Status"
            )


            status = doc.get(
                "status",
                "unknown"
            )


            if status == "approved":

                st.success(
                    status
                )


            elif status == "review_required":

                st.warning(
                    status
                )


            else:

                st.info(
                    status
                )


        # -----------------------------
        # Confidence
        # -----------------------------

        with col2:

            st.write(
                "Confidence"
            )


            confidence = doc.get(
                "confidence",
                0
            )


            try:

                confidence = float(
                    confidence
                )


                st.write(
                    f"{confidence * 100:.2f}%"
                )


            except (
                TypeError,
                ValueError
            ):

                st.write(
                    "N/A"
                )


        # -----------------------------
        # Document ID
        # -----------------------------

        with col3:

            st.write(
                "Document ID"
            )


            st.write(
                doc.get(
                    "id",
                    "N/A"
                )
            )


        # -----------------------------
        # Invoice Data
        # -----------------------------

        with st.expander(
            "View Extracted Invoice Data"
        ):

            invoice_data = doc.get(
                "invoice_data"
            )


            if invoice_data:

                st.json(
                    invoice_data
                )


            else:

                st.info(
                    "No extracted data available."
                )


        # -----------------------------
        # Human Review Data
        # -----------------------------

        reviewed_data = doc.get(
            "reviewed_data"
        )


        if reviewed_data:

            with st.expander(
                "View Human Review Data"
            ):

                st.json(
                    reviewed_data
                )