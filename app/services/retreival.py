from app.services.createVectorStore import get_collection
from app.services.createEmbeddings import embed_query


def retrieve_documents(
    query: str,
    doc_id: int,
    top_k: int = 4,
    score_threshold: float = 0.3
):
    query_embedding = embed_query(query)

    collection = get_collection()  # ✅ fixed

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            where={"doc_id": doc_id},  # ✅ safer
            n_results=top_k
        )

        if not results or not results.get("documents") or not results["documents"][0]:
            return []

        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]

        retrieved_docs = []

        for doc, distance, metadata, _id in zip(documents, distances, metadatas, ids):
            score = 1 - distance if distance is not None else 0

            if score > score_threshold:
                retrieved_docs.append({
                    "id": _id,
                    "content": doc,
                    "score": score,
                    "metadata": {
                        "doc_id": metadata.get("doc_id"),
                        "chunk_index": metadata.get("chunk_index"),
                    }
                })

        # 🔥 fallback if nothing passes threshold
        if not retrieved_docs:
            return [
                {
                    "id": _id,
                    "content": doc,
                    "score": 1 - distance if distance else 0,
                    "metadata": metadata
                }
                for doc, distance, metadata, _id in zip(documents, distances, metadatas, ids)
            ]

        return retrieved_docs

    except Exception as e:
        print(f"Error occurred while retrieving documents: {e}")
        return []