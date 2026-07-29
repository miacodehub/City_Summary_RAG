import faiss
import json
from pathlib import Path

INDEX_DIR = Path(__file__).parent / "indices"
INDEX_DIR.mkdir(exist_ok=True)

INDEX_PATH = INDEX_DIR / "faiss_index.bin"
METADATA_PATH = INDEX_DIR / "metadata.json"


def build_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings.astype("float32"))

    return index


def save_index(index):

    faiss.write_index(index, str(INDEX_PATH))


def load_index():

    return faiss.read_index(str(INDEX_PATH))


def save_metadata(chunks):

    with open(METADATA_PATH, "w", encoding="utf-8") as f:

        json.dump(chunks, f, indent=4, ensure_ascii=False)


def load_metadata():

    with open(METADATA_PATH, "r", encoding="utf-8") as f:

        return json.load(f)