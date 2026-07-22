import os
import time
import logging
import threading
from typing import Optional
from config import settings
from db_manager import db_pool, get_db_cursor

logger = logging.getLogger("saarthi.services")

class EmbeddingService:
    """Singleton Embedding service using sentence-transformers."""
    _model = None
    _lock = threading.Lock()

    def get_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    # sentence-transformers import might take a few seconds
                    from sentence_transformers import SentenceTransformer
                    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}...")
                    start = time.perf_counter()
                    
                    # Hub offline setup
                    os.environ["HF_HUB_OFFLINE"] = "1"
                    self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
                    
                    duration = time.perf_counter() - start
                    logger.info(f"Embedding model loaded successfully in {duration:.2f}s.")
        return self._model

    def encode(self, texts: list) -> list:
        model = self.get_model()
        return model.encode(texts, show_progress_bar=False)

class ChromaManager:
    """Singleton client and collection provider for ChromaDB."""
    _client = None
    _collections = {}
    _lock = threading.Lock()

    def get_client(self):
        if self._client is None:
            with self._lock:
                if self._client is None:
                    import chromadb
                    logger.info(f"Connecting to ChromaDB at: {settings.CHROMA_DIR}...")
                    self._client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
                    logger.info("ChromaDB persistent client initialized successfully.")
        return self._client

    def get_collection(self, name: str):
        client = self.get_client()
        # Ensure knowledge_base requests map to saarthi_kb if saarthi_kb holds the ingested chunks
        if name == "knowledge_base":
            try:
                saarthi_col = client.get_or_create_collection("saarthi_kb")
                if saarthi_col.count() > 0:
                    name = "saarthi_kb"
            except Exception:
                pass
        if name not in self._collections:
            with self._lock:
                if name not in self._collections:
                    logger.info(f"Accessing collection: {name}...")
                    self._collections[name] = client.get_or_create_collection(name)
        return self._collections[name]

    def close(self):
        """Hook to close client on shutdown."""
        with self._lock:
            if self._client is not None:
                # Chroma doesn't have an explicit close in standard clients, 
                # but we clear the cache reference
                self._client = None
                self._collections.clear()
                logger.info("ChromaDB manager resources released.")

class RAGService:
    """Central RAG orchestration service."""
    def __init__(
        self,
        db_manager = None,
        chroma_manager: Optional[ChromaManager] = None,
        embedding_service: Optional[EmbeddingService] = None
    ):
        self.chroma_manager = chroma_manager or ChromaManager()
        self.embedding_service = embedding_service or EmbeddingService()

    def embed_and_query_user_docs(self, session_id: str, conversation_id: str, query_vector: list, n: int = 6) -> list:
        collection = self.chroma_manager.get_collection("user_docs")
        where_clause = {
            "$and": [
                {"session_id": session_id},
                {"conversation_id": conversation_id}
            ]
        }
        
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=n,
            where=where_clause,
            include=["documents", "metadatas", "distances", "embeddings"]
        )
        return results

    def embed_and_query_kb(self, query_vector: list, domain: str, language: str, n: int = 6) -> list:
        collection = self.chroma_manager.get_collection("knowledge_base")
        where_clause = {
            "$and": [
                {"domain": domain},
                {"language": language}
            ]
        }
        
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=n,
            where=where_clause,
            include=["documents", "metadatas", "distances", "embeddings"]
        )
        return results

# Singleton Service Container instances
embedding_service = EmbeddingService()
chroma_manager = ChromaManager()
rag_service = RAGService(chroma_manager=chroma_manager, embedding_service=embedding_service)
