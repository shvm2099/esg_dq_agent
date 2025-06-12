# ESG Document Quality Agent

This project provides an end-to-end workflow for analysing and improving ESG documents.
It consists of a FastAPI backend that processes uploaded files and a Streamlit
frontend for interaction.

## Features
- **Tone calibration**: refines the language of the report using generative models.
- **Structure validation**: reorganises the document into professional sections.
- **Compliance checks**: evaluates alignment with GRI, EU CSRD and SASB
  standards and generates a detailed compliance report.
- **Metadata extraction**: labels each paragraph with relevant ESG tags using
  zero-shot classification.
- **PDF generation**: produces a polished PDF of the revised text.
- **Streamlit interface**: upload PDF, DOCX or TXT files, view the revised text
  and download the generated PDF, metadata and compliance report. Compliance
  scores are displayed with gauge charts.

## Getting Started
1. Install dependencies with `pip install -r requirements.txt` or create the
   conda environment from `environemnt.yml`.
2. Ensure the environment variable `GEMINI_API_KEY` is set for Google Gemini
   access. Optionally define `BASE_URL` for the frontend.
3. Start the backend:
   ```bash
   bash uvicorn_start.sh
   ```
4. Launch the frontend:
   ```bash
   streamlit run frontend/app.py
   ```

Uploaded documents will be processed and the results, files and compliance
scores will be available through the Streamlit UI.
