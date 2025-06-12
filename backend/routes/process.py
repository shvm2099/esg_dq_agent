from fastapi import APIRouter, UploadFile, File
from backend.agents.agent_router import route_to_agent
from backend.file_handler import extract_text
from backend.agents.pdf_generator import generate_pdf

router = APIRouter()

@router.post("/process")
async def process_file(file: UploadFile = File(...)):
    raw_text = await extract_text(file)
    (
        processed_text,
        metadata_filename,
        compliance_filename,
        gri_score,
        eu_csrd_score,
        sasb_score,
    ) = route_to_agent(raw_text)

    pdf_filename = generate_pdf(processed_text)
    pdf_url = f"/pdfs/{pdf_filename}"


    return {
        "processed_text": processed_text,
        "pdf_path": pdf_filename,
        "metadata_path": metadata_filename,
        "compliance_path": compliance_filename,
        "gri_score": gri_score,
        "eu_csrd_score": eu_csrd_score,
        "sasb_score": sasb_score
    }
