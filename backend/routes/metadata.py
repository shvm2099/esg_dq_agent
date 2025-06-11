from fastapi import APIRouter, UploadFile, File
from backend.file_handler import extract_text_from_file
from backend.agents.tone_agent import calibrate_tone
from backend.agents.structure_validator import validate_structure
from backend.agents.metadata_agent import extract_metadata
from backend.rag.rag_suggest import generate_suggested_headers

router = APIRouter()

@router.post("/extract-metadata/")
async def extract_metadata_route(file: UploadFile = File(...)):
    raw_text = await extract_text_from_file(file)
    cal_text = calibrate_tone(raw_text)
    suggestions = generate_suggested_headers(cal_text)
    stru_text = validate_structure(cal_text, suggestions)
    metadata_filename = extract_metadata(stru_text)
    return {"metadata_path": metadata_filename}
