import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv



# Load Environment Variables


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    PROJECT_ROOT / ".env"
)


API_URL = os.getenv(
    "API_URL",
    "http://backend:8000"
)



# Page Title


st.title(
    "Human Review Queue"
)



# Get Review Queue


try:

    response = requests.get(
        f"{API_URL}/review/",
        timeout=5
    )


    if response.status_code != 200:

        st.error(
            "Unable to load review queue."
        )

        st.stop()


    reviews = response.json()


except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to LedgerLens backend. "
        "Make sure FastAPI is running."
    )

    st.stop()


except requests.exceptions.Timeout:

    st.error(
        "Backend request timed out."
    )

    st.stop()


except Exception as e:

    st.error(
        f"Review queue error: {str(e)}"
    )

    st.stop()



# Display Review Queue


if not reviews:

    st.success(
        "No pending reviews."
    )


else:

    for item in reviews:

        st.divider()


        document_id = item.get(
            "id"
        )


        st.warning(
            f"Document ID: {document_id}"
        )


        st.write(
            f"Filename: "
            f"{item.get('filename', 'Unknown')}"
        )


        st.write(
            f"Confidence: "
            f"{item.get('confidence', 'N/A')}"
        )


        invoice_data = item.get(
            "invoice_data",
            {}
        )


        reviewed_data = {}


        st.subheader(
            "Review Invoice Data"
        )


        
        # Editable Invoice Fields
        

        for field, value in invoice_data.items():

            if isinstance(
                value,
                dict
            ):

                current_value = value.get(
                    "value",
                    ""
                )

            else:

                current_value = value


            updated_value = st.text_input(

                field.replace(
                    "_",
                    " "
                ).title(),

                value=str(
                    current_value
                ),

                key=(
                    f"{document_id}_{field}"
                )

            )


            reviewed_data[field] = {

                "value": updated_value,

                "confidence": 1.0

            }


        
        # Approve Invoice
        

        if st.button(

            "Approve Invoice",

            key=(
                f"approve_{document_id}"
            )

        ):

            payload = {

                "document_id": document_id,

                "reviewed_data": reviewed_data

            }


            try:

                approval_response = requests.post(

                    f"{API_URL}/approve/",

                    json=payload,

                    timeout=10

                )


                if approval_response.status_code == 200:

                    st.success(
                        "Invoice approved successfully."
                    )


                    st.json(
                        approval_response.json()
                    )


                    st.rerun()


                else:

                    st.error(

                        "Approval failed: "
                        f"{approval_response.text}"

                    )


            except requests.exceptions.ConnectionError:

                st.error(

                    "Cannot connect to LedgerLens backend."

                )


            except requests.exceptions.Timeout:

                st.error(

                    "Approval request timed out."

                )


            except Exception as e:

                st.error(

                    f"Approval error: {str(e)}"

                )