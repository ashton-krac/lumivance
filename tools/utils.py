import os
from pathlib import Path

# Absolute path to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_PATH = PROJECT_ROOT / "memory"
SRC_PATH = PROJECT_ROOT / "src"
BIBLE_PATH = PROJECT_ROOT / "bible"

def get_params():
    """Returns common parameters for ChromaDB/Ingestion."""
    return {
        "collection_name": "lumivance_knowledge",
        "embedding_model": "text-embedding-3-small"
    }
