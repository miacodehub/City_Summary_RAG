from .embedding import model
from .storage import load_index, load_metadata




def retrieve(city, user_prompt, k=3):

    index = load_index()
    metadata = load_metadata()

    query_embedding = model.encode(
        user_prompt,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = query_embedding.reshape(1, -1)

    # Search more than k because we'll filter afterwards
    scores, indices = index.search(
        query_embedding.astype("float32"),
        20
    )

    results = []

    for idx in indices[0]:

        chunk = metadata[idx]

        if chunk["city"].lower() == city.lower():
            results.append(chunk)

        if len(results) == k:
            break

    return results
    return results

if __name__ == "__main__":

    results = retrieve("I like photography and nature")

    for i, chunk in enumerate(results, start=1):
        print(f"Result {i}")
        print(chunk)
        print("-" * 60)