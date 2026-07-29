#step -1 of RAG
#INGESTION

import json
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"

def load_documents():
    documents = [] # a list
    for file in DATA_DIR.glob("*.json"):
        with open(file, "r", encoding = "utf-8") as f:
            documents.append(json.load(f))
    return documents

def chunk_document(document):

    chunks = []

    city = document["city"]

    for doc in document["documents"]:

        chunks.append(
            {
                "city": city,
                "section": doc["section"],
                "text": f"{doc['section']}: {doc['content']}"
            }
        )

    return chunks
    
def ingest_documents():

    all_chunks = []

    documents = load_documents()

    for document in documents:
        all_chunks.extend(chunk_document(document))

    return all_chunks


if __name__ == "__main__":

    chunks = ingest_documents()

    for chunk in chunks:
        print(chunk)