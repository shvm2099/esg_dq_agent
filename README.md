# ESG Document Quality Agent

This an end-to-end project for analysing and improving ESG documents.
It consists of a FastAPI backend that processes uploaded files and a Streamlit
frontend for interaction.

## Features
- **Tone calibration**: refines the language of the report using generative models.
- **RAG based semantic retrival**: 
- **Structure validation**: reorganises the document into professional sections.
- **Compliance checks**: evaluates alignment with GRI, EU CSRD and SASB
  standards and generates a detailed compliance report.
- **Metadata extraction**: labels each paragraph with relevant ESG tags using
  zero-shot classification.

- **PDF generation**: produces a polished PDF of the revised text.
- **Streamlit interface**: upload PDF, DOCX or TXT files, view the revised text
  and download the generated PDF, metadata and compliance report. Compliance
  scores are displayed with gauge charts.

## Running the code
1. Install dependencies from requirements.txt, remove the ones with @ routes to conda if you face any issues downloading them

2. Create a environment file (.env) and store 
- gemini api key (GEMINI_API_KEY=) the gemini key must have access to gemini 2.0 flash, no quotes
- base url (BASE_URL=), no quotes

3. Start the backend:
>bash uvicorn_start.sh

4. Launch the frontend on another terminal:
>streamlit run frontend/app.py

## Important Information for v-env
- Use python version 3.10 
- add os.environ["USE_TF"] = "1"
os.environ["USE_TORCH"] = "0"


Uploaded documents will be processed and the results, files and compliance
scores will be available through the Streamlit UI.
