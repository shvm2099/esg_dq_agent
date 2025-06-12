import streamlit as sit
import requests
import os
from PIL import Image
from dotenv import load_dotenv
import re
import plotly.graph_objects as go

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

sit.set_page_config(
    page_title="ESG Document Quality Agent", 
    layout="wide",
    initial_sidebar_state="expanded",
)

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

def gauge_chart(value: float, label: str) -> None:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": label},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 50], "color": "red"},
                    {"range": [40, 60], "color": "orange"},
                    {"range": [60, 80], "color": "yellow"},
                    {"range": [80, 100], "color": "green"},
                ],
            },
        )
    )
    fig.update_layout(width=300, height=225, margin=dict(l=20, r=20, t=40, b=0))
    sit.sidebar.plotly_chart(fig, use_container_width=False)

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

    if any(score is not None for score in (gri_score, eu_csrd_score, sasb_score)):
        sit.sidebar.subheader("Compliance Scores")

    if gri_score is not None:
        sit.sidebar.write(f"GRI Compliance Score: {gri_score}%")
        gauge_chart(gri_score, "GRI Compliance Score")

    if eu_csrd_score is not None:
        sit.sidebar.write(f"EU CSRD Compliance Score: {eu_csrd_score}%")
        gauge_chart(eu_csrd_score, "EU CSRD Compliance Score")

    if sasb_score is not None:
        sit.sidebar.write(f"SASB Compliance Score: {sasb_score}%")
        gauge_chart(sasb_score, "SASB Compliance Score")
