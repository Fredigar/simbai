"""
SIMBA Backend - Documents API Routes

Document upload and management endpoints.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories import DocumentRepository
from app.services.rag import RAGService
from app.services.file_processing import FileExtractorFactory
from app.models.document import Document, DocumentListItem
from app.utils.logger import logger


router = APIRouter(prefix="/documents", tags=["documents"])


class UploadResponse(BaseModel):
    """Response after uploading document"""
    document_id: str
    filename: str
    mime_type: str
    size_bytes: int
    indexed: bool
    num_chunks: int


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    conversation_id: str,
    file: UploadFile = File(...),
    auto_index: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a document and optionally index it for RAG.

    Args:
        conversation_id: Conversation ID to associate with
        file: Uploaded file
        auto_index: Whether to automatically index for RAG
        db: Database session

    Returns:
        Upload response with document info
    """
    try:
        # Read file
        file_bytes = await file.read()
        file_size = len(file_bytes)

        logger.info(f"Uploading file: {file.filename} ({file_size} bytes)")

        # Extract text content
        content = FileExtractorFactory.extract(file_bytes, file.content_type)

        # Create document in database
        doc_repo = DocumentRepository(db)
        document = await doc_repo.create(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            filename=file.filename,
            mime_type=file.content_type,
            size_bytes=file_size,
            content=content,
            doc_metadata={"original_name": file.filename},
            vector_ids=[]
        )

        # Index for RAG if requested
        num_chunks = 0
        if auto_index and content and not content.startswith("[Error"):
            rag_service = RAGService(db)
            vector_ids = await rag_service.index_document(
                document_id=document.id,
                conversation_id=conversation_id,
                content=content,
                metadata={
                    "filename": file.filename,
                    "mime_type": file.content_type
                }
            )

            # Update document with vector IDs
            await doc_repo.update(document.id, vector_ids=vector_ids)
            num_chunks = len(vector_ids)
            logger.info(f"Indexed document {document.id} with {num_chunks} chunks")

        return UploadResponse(
            document_id=document.id,
            filename=file.filename,
            mime_type=file.content_type,
            size_bytes=file_size,
            indexed=num_chunks > 0,
            num_chunks=num_chunks
        )

    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/conversation/{conversation_id}", response_model=List[DocumentListItem])
async def get_conversation_documents(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get documents for a conversation.

    Args:
        conversation_id: Conversation ID
        limit: Maximum documents to return
        offset: Offset for pagination
        db: Database session

    Returns:
        List of documents
    """
    try:
        doc_repo = DocumentRepository(db)
        documents = await doc_repo.get_by_conversation(
            conversation_id,
            skip=offset,
            limit=limit
        )

        return [
            DocumentListItem(
                id=doc.id,
                filename=doc.filename,
                mime_type=doc.mime_type,
                size_bytes=doc.size_bytes,
                uploaded_at=doc.uploaded_at,
                indexed=len(doc.vector_ids) > 0
            )
            for doc in documents
        ]

    except Exception as e:
        logger.error(f"Get documents error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get documents: {str(e)}"
        )


@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get document by ID.

    Args:
        document_id: Document ID
        db: Database session

    Returns:
        Document
    """
    try:
        doc_repo = DocumentRepository(db)
        document = await doc_repo.get(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        return Document.model_validate(document)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get document error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get document: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete document.

    Args:
        document_id: Document ID
        db: Database session

    Returns:
        Success status
    """
    try:
        doc_repo = DocumentRepository(db)
        document = await doc_repo.get(document_id)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Delete vectors from ChromaDB if indexed
        if document.vector_ids:
            rag_service = RAGService(db)
            await rag_service.delete_document_vectors(
                conversation_id=document.conversation_id,
                vector_ids=document.vector_ids
            )

        # Delete from database
        await doc_repo.delete(document_id)

        return {"status": "deleted", "document_id": document_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete document error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )
