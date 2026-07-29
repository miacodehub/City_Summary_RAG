from .ingestion import ingest_documents
from .embedding import embed_documents
from .storage import (
    build_index,
    save_index,
    save_metadata
)

chunks = ingest_documents()

embeddings = embed_documents(chunks)

index = build_index(embeddings)

save_index(index)

save_metadata(chunks)

print("Done!")