from backend.agents.tone_agent import calibrate_tone
from backend.agents.structure_validator import validate_structure
from backend.agents.metadata_agent import extract_metadata
from backend.agents.regulatory_agent import (
    check_all_compliance,
    save_compliance_report,
)
from backend.rag.rag_suggest import generate_suggested_headers
def route_to_agent(text: str):
    """Run the full processing pipeline on ``text``."""

    cal_text = calibrate_tone(text)

    suggestions = generate_suggested_headers(cal_text)
    stru_text = validate_structure(cal_text, suggestions)

    metadata_filename = extract_metadata(stru_text)

    compliance_report = check_all_compliance(stru_text)
    compliance_filename = save_compliance_report(compliance_report)

    gri_score = compliance_report.get("gri_score", 0)
    eu_csrd_score = compliance_report.get("eu_csrd_score", 0)
    sasb_score = compliance_report.get("sasb_score", 0)

    return (
        stru_text,
        metadata_filename,
        compliance_filename,
        gri_score,
        eu_csrd_score,
        sasb_score,
    )
