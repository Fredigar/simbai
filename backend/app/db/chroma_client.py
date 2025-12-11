"""
SIMBA Backend - ChromaDB Client

ChromaDB client for vector embeddings and semantic search.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

from app.config import settings
from app.utils.logger import logger


class ChromaDBClient:
    """
    ChromaDB client wrapper for vector operations.

    Provides methods for:
    - Adding documents with embeddings
    - Querying similar documents
    - Managing collections
    """

    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        # Default collection name
        self.collection_name = "simba_documents"
        self.collection = None

        logger.info(f"ChromaDB client initialized: {settings.chroma_url}")

    def get_or_create_collection(self, name: Optional[str] = None):
        """Get or create a collection"""
        collection_name = name or self.collection_name

        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "SIMBA document embeddings"}
            )
            logger.info(f"Collection '{collection_name}' ready")
            return self.collection
        except Exception as e:
            logger.error(f"Error getting/creating collection: {e}")
            raise

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Add documents to collection.

        Args:
            ids: Unique IDs for each document
            documents: Text content
            embeddings: Vector embeddings
            metadatas: Optional metadata dicts
        """
        if not self.collection:
            self.get_or_create_collection()

        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            logger.info(f"Added {len(ids)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            raise

    def query(
        self,
        query_embeddings: List[List[float]],
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        include: List[str] = ["documents", "metadatas", "distances"]
    ) -> Dict[str, Any]:
        """
        Query for similar documents.

        Args:
            query_embeddings: Query vector embeddings
            n_results: Number of results to return
            where: Filter conditions
            include: What to include in results

        Returns:
            Dict with ids, documents, metadatas, distances
        """
        if not self.collection:
            self.get_or_create_collection()

        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where,
                include=include
            )
            logger.info(f"ChromaDB query returned {len(results['ids'][0])} results")
            return results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            raise

    def delete(self, ids: List[str]):
        """Delete documents by IDs"""
        if not self.collection:
            self.get_or_create_collection()

        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from ChromaDB")
        except Exception as e:
            logger.error(f"Error deleting documents from ChromaDB: {e}")
            raise

    def count(self) -> int:
        """Get count of documents in collection"""
        if not self.collection:
            self.get_or_create_collection()

        return self.collection.count()

    def reset_collection(self):
        """Reset (delete all) collection"""
        if not self.collection:
            self.get_or_create_collection()

        try:
            self.client.delete_collection(self.collection_name)
            logger.warning(f"Collection '{self.collection_name}' deleted")
            self.collection = None
            self.get_or_create_collection()
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            raise

    def healthcheck(self) -> bool:
        """Check if ChromaDB is accessible"""
        try:
            self.client.heartbeat()
            return True
        except Exception as e:
            logger.error(f"ChromaDB healthcheck failed: {e}")
            return False


# Singleton instance
chroma_client = ChromaDBClient()


# Dependency for FastAPI
def get_chroma_client() -> ChromaDBClient:
    """Dependency that provides ChromaDB client"""
    return chroma_client
