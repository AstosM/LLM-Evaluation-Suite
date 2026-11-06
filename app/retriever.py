
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "chroma_db"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="llm_knowledge_base",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}
)


def chunk_text(
    text: str,
    chunk_size: int = 120,
    overlap: int = 20
) -> list[str]:

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


def index_document(text: str, source: str) -> int:

    chunks = chunk_text(text)

    if not chunks:
        return 0

    ids = [
        f"{source}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": source,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)


def retrieve_context(
    query: str,
    n_results: int = 3
) -> list[dict]:

    if not query.strip() or collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]

    retrieved = []

    for document, metadata in zip(
        documents[0],
        metadatas[0]
    ):
        retrieved.append({
            "text": document,
            "source": metadata.get("source", "unknown")
        })

    return retrieved
