import os
import time
import logging
import threading
from typing import Optional
from config import settings
from db_manager import db_pool, get_db_cursor

# Safe DTensor monkeypatch for PyTorch / Transformers compatibility
try:
    import torch
    import torch.distributed
    try:
        import torch.distributed.tensor
        if not hasattr(torch.distributed.tensor, "DTensor"):
            class DTensor: pass
            torch.distributed.tensor.DTensor = DTensor
    except Exception:
        pass
except Exception:
    pass

logger = logging.getLogger("saarthi.services")

class EmbeddingService:
    """Singleton Embedding service using sentence-transformers with CUDA/CPU fallback."""
    _model = None
    _lock = threading.Lock()

    def get_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}...")
                    start = time.perf_counter()
                    
                    try:
                        from sentence_transformers import SentenceTransformer
                    except ImportError as ie:
                        logger.error(f"Failed to import SentenceTransformer: {ie}")
                        raise ie

                    # Attempt loading model with CUDA fallback to CPU if GPU OOM/NVML error occurs
                    device = "cpu"
                    try:
                        import torch
                        if torch.cuda.is_available():
                            try:
                                # Test memory allocation
                                torch.cuda.empty_cache()
                                device = "cuda"
                            except Exception as dev_err:
                                logger.warning(f"CUDA available but memory check failed ({dev_err}). Falling back to CPU.")
                                device = "cpu"
                    except Exception:
                        device = "cpu"

                    try:
                        # Try loading with offline local files first to avoid HuggingFace network latency
                        self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, device=device, local_files_only=True)
                    except Exception:
                        try:
                            # Fallback to online/cached load if local_files_only flag fails
                            self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, device=device)
                        except Exception as e:
                            logger.warning(f"Failed loading model on device '{device}': {e}. Retrying on CPU...")
                            try:
                                if "HF_HUB_OFFLINE" in os.environ:
                                    del os.environ["HF_HUB_OFFLINE"]
                                self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, device="cpu")
                            except Exception as ex:
                                logger.error(f"Critical error loading embedding model on CPU: {ex}")
                                raise ex
                    
                    duration = time.perf_counter() - start
                    logger.info(f"Embedding model loaded successfully on '{getattr(self._model, 'device', 'cpu')}' in {duration:.2f}s.")
        return self._model

    def encode(self, texts: list) -> list:
        try:
            model = self.get_model()
            embeddings = model.encode(texts, show_progress_bar=False)
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except Exception:
                pass
            return embeddings
        except Exception as e:
            logger.error(f"Embedding encode error: {e}")
            raise e

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

    def get_total_chunk_count(self) -> int:
        """Returns aggregate chunk count across all knowledge base & document collections."""
        total = 0
        try:
            client = self.get_client()
            for col_name in ["knowledge_base", "saarthi_kb", "user_docs"]:
                try:
                    col = client.get_or_create_collection(col_name)
                    total += col.count()
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Error computing total chunk count: {e}")
        return total

    def close(self):
        """Hook to close client on shutdown."""
        with self._lock:
            if self._client is not None:
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
        
        where_conditions = [{"session_id": session_id}]
        if conversation_id and conversation_id != "new":
            where_conditions.append({"conversation_id": conversation_id})
            
        where_clause = {"$and": where_conditions} if len(where_conditions) > 1 else where_conditions[0]
        
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

