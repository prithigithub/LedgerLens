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
    "Upload Invoice"
)


# -----------------------------
# Choose Invoice Image
# -----------------------------

uploaded_file = st.file_uploader(

    "Choose invoice image",

    type=[
        "png",
        "jpg",
        "jpeg",
    ],

)


# -----------------------------
# Display Selected Image
# -----------------------------

if uploaded_file:

    st.image(

        uploaded_file,

        caption=uploaded_file.name,

        width=400,

    )


    # -----------------------------
    # Process Invoice
    # -----------------------------

    if st.button(

        "Process Invoice"

    ):

        try:

            files = {

                "file": (

                    uploaded_file.name,

                    uploaded_file.getvalue(),

                    uploaded_file.type,

                )

            }


            with st.spinner(

                "Processing invoice..."

            ):

                response = requests.post(

                    f"{API_URL}/ingest/",

                    files=files,

                    timeout=120,

                )


            if response.status_code == 200:

                result = response.json()


                st.success(

                    "Invoice processed successfully"

                )


                st.subheader(

                    "Processing Result"

                )


                st.json(

                    result

                )


            else:

                st.error(

                    "Invoice processing failed: "

                    f"{response.text}"

                )


        except requests.exceptions.ConnectionError:

            st.error(

                "Cannot connect to backend. "

                "Start FastAPI first."

            )


        except requests.exceptions.Timeout:

            st.error(

                "Processing took too long. "

                "Try again."

            )


        except Exception as e:

            st.error(

                f"Unexpected error: {str(e)}"

            )