import json
import os
import unicodedata
import re
from src.ingestion.utils import save_jsonl

INPUT_FILE = "data/processed/raw_documents.jsonl"
OUTPUT_FILE = "data/processed/clean_documents.jsonl"

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFKC", text)

def fix_ligatures(text: str) -> str:
    ligatures = {
        "\ufb00": "ff",
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\ufb03": "ffi",
        "\ufb04": "ffl",
        "\ufb05": "ft",
        "\ufb06": "st",
    }

    for code, val in ligatures.items():
        text = text.replace(code, val)
    return text

def remove_noise(text: str) -> str:
    noise_patterns = [
        "Log in",
        "Fidelity Learn",
        "Save Share",
        "Print"
    ]

    for n in noise_patterns:
        text = text.replace(n, "")

    return text

def fix_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_text(text: str) -> str:
    text = normalize_text(text)
    text = fix_ligatures(text)
    text = remove_noise(text)
    text = fix_spacing(text)
    return text

def process_documents():
    cleaned_docs = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)

            cleaned_text = clean_text(doc["text"])

            cleaned_docs.append({
                "doc_id": doc["doc_id"],
                "text": cleaned_text,
                "metadata": doc["metadata"]
            })

    return cleaned_docs

if __name__ == "__main__":
    docs = process_documents()
    save_jsonl(docs, OUTPUT_FILE)
    print(f"Saved {len(docs)} cleaned documents to {OUTPUT_FILE}")