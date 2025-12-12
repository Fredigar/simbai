"""
SIMBA Backend - RAG API Routes

RAG endpoints for document indexing and semantic search.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.rag import RAGService
from app.repositories import DocumentRepository
from app.models.message import Source
from app.utils.logger import logger


router = APIRouter(prefix="/rag", tags=["rag"])


# Request/Response models
class IndexDocumentRequest(BaseModel):
    """Request to index a document"""
    document_id: str
    conversation_id: str
    content: str
    metadata: Optional[dict] = Field(default_factory=dict)
    chunk_size: int = Field(500, ge=100, le=2000)
    chunk_overlap: int = Field(50, ge=0, le=500)


class IndexDocumentResponse(BaseModel):
    """Response after indexing"""
    document_id: str
    vector_ids: List[str]
    num_chunks: int


class SearchRequest(BaseModel):
    """Request to search documents"""
    conversation_id: str
    query: str = Field(..., min_length=1, max_length=1000)
    n_results: int = Field(5, ge=1, le=20)
    min_score: float = Field(0.0, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Search results"""
    query: str
    sources: List[Source]
    total_found: int


@router.post("/index", response_model=IndexDocumentResponse)
async def index_document(
    request: IndexDocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Index a document for semantic search.

    Args:
        request: Index request with document content
        db: Database session

    Returns:
        Index response with vector IDs
    """
    try:
        rag_service = RAGService(db)

        vector_ids = await rag_service.index_document(
            document_id=request.document_id,
            conversation_id=request.conversation_id,
            content=request.content,
            metadata=request.metadata,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )

        return IndexDocumentResponse(
            document_id=request.document_id,
            vector_ids=vector_ids,
            num_chunks=len(vector_ids)
        )

    except Exception as e:
        logger.error(f"Index error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index document: {str(e)}"
        )


@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic search for relevant documents.

    Args:
        request: Search request with query
        db: Database session

    Returns:
        Search results with sources
    """
    try:
        rag_service = RAGService(db)

        sources = await rag_service.search(
            conversation_id=request.conversation_id,
            query=request.query,
            n_results=request.n_results,
            min_score=request.min_score
        )

        return SearchResponse(
            query=request.query,
            sources=sources,
            total_found=len(sources)
        )

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.delete("/documents/{document_id}")
async def delete_document_vectors(
    document_id: str,
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete document vectors from ChromaDB.

    Args:
        document_id: Document ID
        conversation_id: Conversation ID
        db: Database session

    Returns:
        Success status
    """
    try:
        # Get document to find vector IDs
        doc_repo = DocumentRepository(db)
        document = await doc_repo.get(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Delete vectors
        rag_service = RAGService(db)
        success = await rag_service.delete_document_vectors(
            conversation_id=conversation_id,
            vector_ids=document.vector_ids
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete vectors"
            )

        return {"status": "deleted", "document_id": document_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}"
        )
