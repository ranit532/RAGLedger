"""
Query router - handles RAG queries
"""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest, QueryResponse
from services.query_service import QueryService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query documents using RAG: retrieve relevant chunks and generate answer
    """
    try:
        query_service = QueryService()
        
        # Process the query
        result = await query_service.query(
            query=request.query,
            top_k=request.top_k
        )
        
        return QueryResponse(
            answer=result['answer'],
            sources=result['sources'],
            query=request.query
        )
    except Exception as e:
        logger.error(f"Error querying documents: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )

