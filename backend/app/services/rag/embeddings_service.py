"""
SIMBA Backend - Embeddings Service

Generate embeddings for text using sentence-transformers.
"""

from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils.logger import logger
from app.config import settings


class EmbeddingsService:
    """Service for generating text embeddings"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embeddings service.

        Args:
            model_name: Name of the sentence-transformers model
                       Default: all-MiniLM-L6-v2 (fast, 384 dimensions)
                       Alternatives: all-mpnet-base-v2 (better quality, 768 dims)
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.dimension: Optional[int] = None

    def _load_model(self):
        """Lazy load the model"""
        if self.model is None:
            logger.info(f"Loading embeddings model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            # Get embedding dimension
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded. Embedding dimension: {self.dimension}")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings
            batch_size: Batch size for encoding

        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        self._load_model()

        if not texts:
            return np.array([])

        logger.info(f"Encoding {len(texts)} texts with batch_size={batch_size}")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=len(texts) > 100,
            convert_to_numpy=True
        )

        return embeddings

    def encode_single(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Text string

        Returns:
            numpy array of shape (embedding_dim,)
        """
        embeddings = self.encode([text])
        return embeddings[0]

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between -1 and 1
        """
        embeddings = self.encode([text1, text2])

        # Cosine similarity
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )

        return float(similarity)

    def get_dimension(self) -> int:
        """Get embedding dimension"""
        self._load_model()
        return self.dimension


# Global instance
_embeddings_service: Optional[EmbeddingsService] = None


def get_embeddings_service() -> EmbeddingsService:
    """Get or create global embeddings service instance"""
    global _embeddings_service

    if _embeddings_service is None:
        model_name = getattr(settings, 'EMBEDDINGS_MODEL', 'all-MiniLM-L6-v2')
        _embeddings_service = EmbeddingsService(model_name=model_name)

    return _embeddings_service
