import os
import json
from datetime import datetime
import spacy
import copy

nlp = spacy.load("en_core_web_sm")

GRI_RULES_PATH = "backend/agents/gri_rules.json"
EU_CSRD_RULES_PATH = "backend/agents/eu_csrd.json"
SASB_RULES_PATH = "backend/agents/sasb.json"

def load_rules(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def preprocess_text(text: str) -> set:
    doc = nlp(text.lower())
    lemmas = {token.lemma_ for token in doc if not token.is_stop and not token.is_punct}
    return lemmas

def check_compliance(text: str, rules: dict) -> dict:

    lemmas = preprocess_text(text)
    report = {}
    total_points = 0
    earned_points = 0

    for code, content in rules.items():
        topic = content.get("topic", "")
        disclosures = content.get("mandatory_disclosures", [])
        topic_report = []

        for disclosure in disclosures:
            found = []
            missing = []
            required_data = disclosure.get("required_data", [])

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
                "id": disclosure.get("id", ""),
                "title": disclosure.get("title", ""),
                "found_data_points": found,
                "missing_data_points": missing,
                "score_percent": round(disclosure_score * 100, 2)
            })

        report[code] = {
            "topic": topic,
            "disclosures": topic_report
        }

    overall_score = round((earned_points / total_points) * 100, 2) if total_points > 0 else 0
    return {
        "overall_score": overall_score,
        "detailed_report": report
    }


def merge_reports(gri_report: dict, eu_csrd_report: dict, sasb_report: dict) -> dict:

    combined_report = copy.deepcopy(gri_report)

    for key, value in eu_csrd_report.items():
        if key in combined_report:
            combined_report[key].update(value)
        else:
            combined_report[key] = value
            
    for key, value in sasb_report.items():
        if key in combined_report:
            combined_report[key].update(value)
        else:
            combined_report[key] = value
            
    return combined_report

def check_keyword_compliance(text: str, keywords: list[str], tag: str) -> dict:
    lemmas = preprocess_text(text)
    found = []
    missing = []

    for term in keywords:
        term_lemmas = preprocess_text(term)
        if term_lemmas & lemmas:
            found.append(term)
        else:
            missing.append(term)

    score = round((len(found) / len(keywords)) * 100, 2) if keywords else 0

    return {
        "overall_score": score,
        "detailed_report": {
            tag: {
                "topic": f"{tag} Key Terms",
                "disclosures": [
                    {
                        "id": tag,
                        "title": "Keyword presence",
                        "found_data_points": found,
                        "missing_data_points": missing,
                        "score_percent": score,
                    }
                ],
            }
        },
    }


def check_all_compliance(text: str):
    gri_rules = load_rules(GRI_RULES_PATH)
    eu_csrd_rules = load_rules(EU_CSRD_RULES_PATH)
    sasb_rules = load_rules(SASB_RULES_PATH)

    gri_result = check_compliance(text, gri_rules)

    eu_keywords = (
        eu_csrd_rules.get("csrd_compliance_rules", {})
        .get("nlp_compliance_keywords", {})
        .get("mandatory_terms", [])
    )
    eu_csrd_result = check_keyword_compliance(text, eu_keywords, "EU_CSRD")

    sasb_keywords = (
        sasb_rules.get("sasb_compliance_rules", {})
        .get("nlp_compliance_keywords", {})
        .get("mandatory_identifiers", [])
    )
    sasb_result = check_keyword_compliance(text, sasb_keywords, "SASB")

    final_report = merge_reports(
        gri_result["detailed_report"],
        eu_csrd_result["detailed_report"],
        sasb_result["detailed_report"],
    )

    combined_result = {
        "gri_score": gri_result["overall_score"],
        "eu_csrd_score": eu_csrd_result["overall_score"],
        "sasb_score": sasb_result["overall_score"],
        "final_report": final_report,
    }

    return combined_result

def save_compliance_report(report: dict, folder="backend/compliance_reports") -> str:
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    filename = f"combined_structured_compliance_{timestamp}.json"
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return filename
