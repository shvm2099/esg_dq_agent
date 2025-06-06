from fastapi import APIRouter, UploadFile, File
from backend.agents.agent_router import route_to_agent
from backend.file_handler import extract_text_from_file
from backend.agents.pdf_generator import generate_pdf

router = APIRouter()

@router.post("/process")
async def process_file(file: UploadFile = File(...)):
    raw_text = await extract_text_from_file(file)
    processed_text, metadata_filename, compliance_filename, overall_score = route_to_agent(raw_text)

    pdf_filename = generate_pdf(processed_text)
    pdf_url = f"/pdfs/{pdf_filename}"


    return {
        "processed_text": processed_text,
        "pdf_path": pdf_filename,
        "metadata_path": metadata_filename,
        "compliance_path": compliance_filename,
        "overall_score": overall_score
    }
