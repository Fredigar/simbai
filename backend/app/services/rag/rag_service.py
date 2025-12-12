"""
SIMBA Backend - RAG Service

Retrieval-Augmented Generation service for semantic search and document retrieval.
"""

import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.chroma_client import get_chroma_client
from app.services.rag.embeddings_service import get_embeddings_service
from app.repositories import DocumentRepository
from app.models.message import Source
from app.utils.logger import logger


class RAGService:
    """RAG service for document indexing and retrieval"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.chroma = get_chroma_client()
        self.embeddings = get_embeddings_service()
        self.document_repo = DocumentRepository(db)

    def _get_collection_name(self, conversation_id: str) -> str:
        """Get ChromaDB collection name for conversation"""
        # Sanitize conversation_id for ChromaDB
        # ChromaDB collection names must be 3-63 chars, alphanumeric + - _
        sanitized = conversation_id.replace('-', '_')
        return f"conv_{sanitized}"

    async def index_document(
        self,
        document_id: str,
        conversation_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> List[str]:
        """
        Index a document into ChromaDB with chunking.

        Args:
            document_id: Document ID
            conversation_id: Conversation ID
            content: Document text content
            metadata: Optional metadata
            chunk_size: Size of text chunks (characters)
            chunk_overlap: Overlap between chunks

        Returns:
            List of vector IDs created
        """
        try:
            logger.info(f"Indexing document {document_id} for conversation {conversation_id}")

            # Get or create collection
            collection_name = self._get_collection_name(conversation_id)
            collection = self.chroma.get_or_create_collection(collection_name)

            # Chunk the content
            chunks = self._chunk_text(content, chunk_size, chunk_overlap)
            logger.info(f"Split document into {len(chunks)} chunks")

            # Generate embeddings
            embeddings = self.embeddings.encode(chunks)

            # Prepare IDs and metadata
            vector_ids = [f"{document_id}_{i}" for i in range(len(chunks))]
            chunk_metadata = [
                {
                    "document_id": document_id,
                    "conversation_id": conversation_id,
                    "chunk_index": i,
                    "chunk_total": len(chunks),
                    **(metadata or {})
                }
                for i in range(len(chunks))
            ]

            # Add to ChromaDB
            collection.add(
                ids=vector_ids,
                embeddings=embeddings.tolist(),
                documents=chunks,
                metadatas=chunk_metadata
            )

            logger.info(f"Indexed {len(vector_ids)} chunks for document {document_id}")
            return vector_ids

        except Exception as e:
            logger.error(f"Error indexing document {document_id}: {e}")
            raise

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            # Get chunk
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < text_len:
                # Look for sentence endings
                last_period = chunk.rfind('. ')
                last_newline = chunk.rfind('\n')
                last_break = max(last_period, last_newline)

                if last_break > chunk_size * 0.5:  # At least 50% of chunk
                    chunk = chunk[:last_break + 1]
                    end = start + last_break + 1

            chunks.append(chunk.strip())

            # Move to next chunk with overlap
            start = end - chunk_overlap

        return [c for c in chunks if c]  # Filter empty chunks

    async def search(
        self,
        conversation_id: str,
        query: str,
        n_results: int = 5,
        min_score: float = 0.0
    ) -> List[Source]:
        """
        Semantic search for relevant documents.

        Args:
            conversation_id: Conversation ID to search within
            query: Search query
            n_results: Maximum number of results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of Source objects with relevant content
        """
        try:
            logger.info(f"Searching in conversation {conversation_id}: '{query[:50]}...'")

            # Get collection
            collection_name = self._get_collection_name(conversation_id)

            try:
                collection = self.chroma.get_collection(collection_name)
            except Exception:
                logger.warning(f"No collection found for conversation {conversation_id}")
                return []

            # Generate query embedding
            query_embedding = self.embeddings.encode_single(query)

            # Search
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )

            # Parse results
            sources = []

            if results and results['ids'] and len(results['ids']) > 0:
                for i, vector_id in enumerate(results['ids'][0]):
                    # Calculate similarity score (1 - distance for cosine)
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    score = 1 - distance

                    if score < min_score:
                        continue

                    metadata = results['metadatas'][0][i] if 'metadatas' in results else {}
                    document = results['documents'][0][i] if 'documents' in results else ""

                    source = Source(
                        id=vector_id,
                        title=f"Chunk {metadata.get('chunk_index', 0) + 1}/{metadata.get('chunk_total', 1)}",
                        content=document[:500],  # Limit excerpt
                        score=score,
                        provider="chromadb",
                        metadata=metadata
                    )
                    sources.append(source)

            logger.info(f"Found {len(sources)} relevant sources")
            return sources

        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

    async def rerank_sources(
        self,
        query: str,
        sources: List[Source],
        top_k: int = 3
    ) -> List[Source]:
        """
        Rerank sources by relevance to query.

        Args:
            query: User query
            sources: List of sources to rerank
            top_k: Number of top sources to return

        Returns:
            Reranked and filtered sources
        """
        if not sources:
            return []

        try:
            logger.info(f"Reranking {len(sources)} sources")

            # Calculate relevance scores
            texts = [query] + [s.content for s in sources]
            embeddings = self.embeddings.encode(texts)

            query_emb = embeddings[0]
            source_embs = embeddings[1:]

            # Calculate similarities
            scores = []
            for i, source_emb in enumerate(source_embs):
                similarity = np.dot(query_emb, source_emb) / (
                    np.linalg.norm(query_emb) * np.linalg.norm(source_emb)
                )
                scores.append((similarity, i))

            # Sort by score
            scores.sort(reverse=True)

            # Get top_k sources
            reranked = [sources[idx] for _, idx in scores[:top_k]]

            # Update scores
            for source, (score, _) in zip(reranked, scores[:top_k]):
                source.score = float(score)

            logger.info(f"Reranked to top {len(reranked)} sources")
            return reranked

        except Exception as e:
            logger.error(f"Error reranking: {e}")
            # Return original sources if reranking fails
            return sources[:top_k]

    async def delete_document_vectors(
        self,
        conversation_id: str,
        vector_ids: List[str]
    ) -> bool:
        """
        Delete document vectors from ChromaDB.

        Args:
            conversation_id: Conversation ID
            vector_ids: List of vector IDs to delete

        Returns:
            True if successful
        """
        try:
            collection_name = self._get_collection_name(conversation_id)
            collection = self.chroma.get_collection(collection_name)

            collection.delete(ids=vector_ids)

            logger.info(f"Deleted {len(vector_ids)} vectors from {collection_name}")
            return True

        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False


# Import numpy for reranking
import numpy as np
