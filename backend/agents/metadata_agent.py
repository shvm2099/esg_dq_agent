from transformers import pipeline
import json
import os
from datetime import datetime
os.environ["USE_TF"] = "1"
os.environ["USE_TORCH"] = "0"
import re

def clean_markdown(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    return text

TAGS = [
    "internal",
    "client-facing",
    "public",
    "environmental",
    "governance",
    "social",
    "carbon emissions",
    "diversity, equity, and inclusion",
    "human rights",
    "sustainable finance",
    "Global Reporting Initiative",
    "energy transition",
    "supply chain",
    "data privacy"]

classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",
    framework="tf")

def extract_metadata(text: str, folder: str = "backend/metadata", threshold: float = 0.4) -> str:
    os.makedirs(folder, exist_ok=True)

    paragraphs = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    results = []

    for i, para in enumerate(paragraphs):

        clean_para = clean_markdown(para)
        result = classifier(
            sequences=clean_para,
            candidate_labels=TAGS,
            multi_label=True)

        filtered = [
            {"label": label, "score": float(score)}
            for label, score in zip(result["labels"], result["scores"])
            if score >= threshold]
        
        results.append({
            "paragraph_index": i,
            "text": clean_para,
            "predicted_tags": filtered})

    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    filename = f"metadata_{timestamp}.json"
    full_path = os.path.join(folder, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump({"paragraphs": results}, f, indent=2, ensure_ascii=False)

    return filename  