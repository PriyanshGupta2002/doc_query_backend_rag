import chromadb
import uuid
from typing import List
from langchain_core.documents import Document

_client = chromadb.PersistentClient(path="./chroma_db")


def get_collection():
    return _client.get_or_create_collection(
        name="doc_query_vector",
        metadata={"hnsw:space": "cosine"}
    )


def create_vector_store(
    embeddings,
    document_chunks: List[Document],
    doc_id: int
):
    collection = get_collection()

    # 🔥 check if this doc already exists
    existing = collection.get(where={"doc_id": doc_id})
    if existing["ids"]:
        print(f"Vector store already exists for doc {doc_id}")
        return

    ids = []
    documents = []
    metadatas = []
    vectors = []

    for i, (doc, embedding) in enumerate(zip(document_chunks, embeddings)):
        ids.append(str(uuid.uuid4()))
        documents.append(doc.page_content)

        metadata = dict(doc.metadata)
        metadata["doc_id"] = doc_id
        metadata["chunk_index"] = i
        metadata["content_length"] = len(doc.page_content)

        metadatas.append(metadata)
        vectors.append(embedding)

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas
    )
