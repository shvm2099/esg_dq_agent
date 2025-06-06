from fastapi import APIRouter, UploadFile, File
from backend.file_handler import extract_text_from_file
from backend.agents.agent_router import calibrate_tone, validate_structure
from backend.agents.metadata_agent import extract_metadata

router = APIRouter()

@router.post("/extract-metadata/")
async def extract_metadata_route(file: UploadFile = File(...)):
    raw_text = await extract_text_from_file(file)
    cal_text = calibrate_tone(raw_text)
    stru_text = validate_structure(cal_text)
    metadata_filename = extract_metadata(stru_text)
    return {"metadata_path": metadata_filename}
