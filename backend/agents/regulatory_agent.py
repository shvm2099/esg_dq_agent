import os
import json
from datetime import datetime
import spacy

nlp = spacy.load("en_core_web_sm")

RULES_PATH = "backend/agents/gri_rules.json"

def load_gri_rules(path: str = RULES_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def preprocess_text(text: str) -> set:
    doc = nlp(text.lower())
    lemmas = {token.lemma_ for token in doc if not token.is_stop and not token.is_punct}
    return lemmas

def check_gri_compliance(text: str, gri_rules: dict) -> dict:
    lemmas = preprocess_text(text)
    report = {}
    total_points = 0
    earned_points = 0

    for gri_code, content in gri_rules.items():
        topic = content["topic"]
        disclosures = content["mandatory_disclosures"]
        topic_report = []

        for disclosure in disclosures:
            found = []
            missing = []
            required_data = disclosure["required_data"]

            for term in required_data:
                term_lemmas = preprocess_text(term)
                if term_lemmas & lemmas:
                    found.append(term)
                else:
                    missing.append(term)

            disclosure_score = len(found) / len(required_data) if required_data else 0
            total_points += len(required_data)
            earned_points += len(found)

            topic_report.append({
                "id": disclosure["id"],
                "title": disclosure["title"],
                "found_data_points": found,
                "missing_data_points": missing,
                "score_percent": round(disclosure_score * 100, 2)
            })

        report[gri_code] = {
            "topic": topic,
            "disclosures": topic_report
        }

    overall_score = round((earned_points / total_points) * 100, 2) if total_points > 0 else 0
    return {
        "overall_score": overall_score,
        "detailed_report": report
    }

def save_compliance_report(report: dict, folder="backend/compliance_reports") -> str:
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    filename = f"gri_structured_compliance_{timestamp}.json"
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return filename


