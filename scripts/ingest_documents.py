import sys
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.retriever import index_document
DOCUMENT_PATH = BASE_DIR / "datasets" / "knowledge_base.txt"


def main():

    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {DOCUMENT_PATH}"
        )

    text = DOCUMENT_PATH.read_text(encoding="utf-8")

    chunks_added = index_document(
        text=text,
        source="knowledge_base"
    )

    print(f"Document ingestion completed.")
    print(f"Chunks indexed: {chunks_added}")


if __name__ == "__main__":
    main()

