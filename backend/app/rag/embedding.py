from sentence_transformers import SentenceTransformer
from .ingestion import ingest_documents

# Load once when the module is imported
model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_documents(chunks):
    """
    Converts all chunk texts into embeddings.

    Args:
        chunks: List of chunk dictionaries.

    Returns:
        numpy.ndarray of shape (num_chunks, embedding_dimension)
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":

    chunks = ingest_documents()

    embeddings = embed_documents(chunks)

    print(embeddings[0][:10])

