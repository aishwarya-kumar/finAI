import os
import json
from pypdf import PdfReader
from src.ingestion.utils import save_jsonl

RAW_DIR = "data/raw"
OUT_FILE = "data/processed/raw_documents.jsonl"

def extract_pdf(file_path: str):
    reader = PdfReader(file_path)

    full_text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text.append(page_text)

    return " ".join(full_text), len(reader.pages)
def process_pdfs():
    documents = []

    for file_name in os.listdir(RAW_DIR):
        if not file_name.endswith(".pdf"):
            continue

        file_path = os.path.join(RAW_DIR, file_name)

        text, num_pages = extract_pdf(file_path)

        doc = {
            "doc_id": file_name,
            "text": text,
            "metadata": {
                "source": "fidelity_learning_center",
                "file_name": file_name,
                "num_pages": num_pages
            }
        }

        documents.append(doc)

    return documents


if __name__ == "__main__":
    docs = process_pdfs()
    save_jsonl(docs, OUT_FILE)
    print(f"Saved {len(docs)} documents to {OUT_FILE}")