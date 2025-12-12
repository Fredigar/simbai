"""
SIMBA Backend - File Content Extractors

Extract text content from various file formats.
"""

import io
from typing import Optional
from pathlib import Path

from app.utils.logger import logger


class PDFExtractor:
    """Extract text from PDF files"""

    @staticmethod
    def extract(file_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            import PyMuPDF as fitz  # type: ignore

            text_parts = []
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text_parts.append(page.get_text())

            pdf_document.close()

            return "\n\n".join(text_parts)

        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return f"[Error extracting PDF: {e}]"


class DocxExtractor:
    """Extract text from DOCX files"""

    @staticmethod
    def extract(file_bytes: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            from docx import Document  # type: ignore

            doc = Document(io.BytesIO(file_bytes))

            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)

            return "\n\n".join(text_parts)

        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return f"[Error extracting DOCX: {e}]"


class TxtExtractor:
    """Extract text from TXT files"""

    @staticmethod
    def extract(file_bytes: bytes) -> str:
        """Extract text from TXT bytes"""
        try:
            # Try UTF-8 first, fall back to latin-1
            try:
                return file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return file_bytes.decode('latin-1', errors='replace')

        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            return f"[Error extracting TXT: {e}]"


class FileExtractorFactory:
    """Factory for getting appropriate extractor"""

    EXTRACTORS = {
        'application/pdf': PDFExtractor,
        'text/plain': TxtExtractor,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxExtractor,
    }

    @classmethod
    def get_extractor(cls, mime_type: str):
        """Get extractor for MIME type"""
        return cls.EXTRACTORS.get(mime_type)

    @classmethod
    def extract(cls, file_bytes: bytes, mime_type: str) -> str:
        """Extract text from file bytes"""
        extractor = cls.get_extractor(mime_type)

        if not extractor:
            logger.warning(f"No extractor for MIME type: {mime_type}")
            return f"[Unsupported file type: {mime_type}]"

        return extractor.extract(file_bytes)
