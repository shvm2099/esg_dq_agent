from backend.agents.tone_agent import calibrate_tone
from backend.agents.structure_validator import validate_structure
from backend.agents.metadata_agent import extract_metadata
from backend.agents.regulatory_agent import (load_gri_rules, check_gri_compliance, save_compliance_report)
def route_to_agent (text : str):
    cal_text = calibrate_tone(text)
    stru_text = validate_structure(cal_text)

    metadata_filename = extract_metadata(text)

    rules = load_gri_rules()
    compliance_report = check_gri_compliance(stru_text, rules)
    compliance_filename = save_compliance_report(compliance_report)
    overall_score = compliance_report.get("overall_score", 0)

    return stru_text, metadata_filename, compliance_filename, overall_score
