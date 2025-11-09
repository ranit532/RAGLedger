"""
Ingest router - handles document ingestion and embedding
"""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import IngestRequest, IngestResponse
from services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """
    Ingest a document: extract text, chunk it, generate embeddings, and store in Pinecone
    """
    try:
        ingestion_service = IngestionService()
        
        # Process the document
        result = await ingestion_service.ingest_document(request.file_id)
        
        return IngestResponse(
            message="Document ingested successfully",
            chunks_processed=result['chunks_processed']
        )
    except Exception as e:
        logger.error(f"Error ingesting document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

