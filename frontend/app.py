import streamlit as sit
import requests
import os
from PIL import Image
from dotenv import load_dotenv
import re

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

sit.set_page_config(page_title="ESG Document Quality", layout="wide")

image_path = "pics/kpmg.png"
if os.path.exists(image_path):
    image = Image.open(image_path)
    sit.image(image, use_container_width=False, width=325)

sit.title("ESG Document Quality Agent")
sit.markdown("Upload your ESG report (PDF, DOCX, or TXT) to enhance its tone, structure, and ensure alignment with GRI compliance standards. Extract detailed metadata for deeper analysis.")


def clean_llm_output(text):
    text = text.replace("**", "")
    return re.sub(r"\*+", "", text)


if "result" not in sit.session_state:
    sit.session_state.result = {}


uploaded_file = sit.file_uploader("Upload your file", type=["pdf", "docx", "txt"])

if sit.button("Start") and uploaded_file:
    with sit.spinner("Processing..."):
        files = {
            "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }

        try:
            response = requests.post(f"{BASE_URL}/process/", files=files)

            if response.status_code == 200:
                sit.session_state.result = response.json()
            else:
                sit.error("Failed to process the document.")
        except requests.exceptions.RequestException as e:
            sit.error(f"Connection error: {e}")


if sit.session_state.result:
    result = sit.session_state.result
    processed_text = clean_llm_output(result.get("processed_text", "[No output returned]"))
    sit.text_area("Output", processed_text, height=650)

    pdf_path = result.get("pdf_path")
    metadata_path = result.get("metadata_path")
    compliance_path = result.get("compliance_path")
    gri_score = result.get("gri_score")
    eu_csrd_score = result.get("eu_csrd_score")
    sasb_score = result.get("sasb_score")

    if pdf_path:
        pdf_url = f"{BASE_URL}/pdfs/{pdf_path}"
        pdf_file = requests.get(pdf_url)
        sit.sidebar.download_button(
            label="Download PDF",
            data=pdf_file.content,
            file_name=pdf_path,
            mime="application/pdf"
        )

    if metadata_path:
        meta_url = f"{BASE_URL}/metadata/{metadata_path}"
        meta_file = requests.get(meta_url)
        sit.sidebar.download_button(
            label="Download Metadata",
            data=meta_file.content,
            file_name=metadata_path,
            mime="application/json"
        )

    if compliance_path:
        comp_url = f"{BASE_URL}/compliance_reports/{compliance_path}"
        comp_file = requests.get(comp_url)
        sit.sidebar.download_button(
            label="Download Compliance Report",
            data=comp_file.content,
            file_name=compliance_path,
            mime="application/json"
        )

    if gri_score is not None:
        sit.sidebar.metric("GRI Compliance Score", f"{gri_score}%")

    if eu_csrd_score is not None:
        sit.sidebar.metric("EU CSRD Compliance Score", f"{eu_csrd_score}%")

    if sasb_score is not None:
        sit.sidebar.metric("SASB Compliance Score", f"{sasb_score}%")
