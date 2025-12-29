import chromadb
from chromadb.config import Settings
from .utils import MEMORY_PATH

def get_client():
    """Returns a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=str(MEMORY_PATH), settings=Settings(allow_reset=True))

def get_collection(client, name="lumivance_knowledge"):
    """Get or create the knowledge collection."""
    return client.get_or_create_collection(name=name)
