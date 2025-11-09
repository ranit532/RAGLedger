"""
Health check router
"""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import HealthResponse
from services.openai_service import OpenAIService
from services.pinecone_service import PineconeService
import boto3

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns the status of the service and its dependencies
    """
    try:
        # Check OpenAI
        openai_status = "unknown"
        try:
            openai_service = OpenAIService()
            # Simple check - just verify the service is initialized
            openai_status = "healthy" if openai_service.client else "unhealthy"
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            openai_status = "unhealthy"

        # Check Pinecone
        pinecone_status = "unknown"
        try:
            pinecone_service = PineconeService()
            # Check if index exists and is accessible
            pinecone_status = "healthy" if pinecone_service.index else "unhealthy"
        except Exception as e:
            logger.error(f"Pinecone health check failed: {e}")
            pinecone_status = "unhealthy"

        # Check S3
        s3_status = "unknown"
        try:
            s3_client = boto3.client('s3')
            s3_client.list_buckets()
            s3_status = "healthy"
        except Exception as e:
            logger.error(f"S3 health check failed: {e}")
            s3_status = "unhealthy"

        return HealthResponse(
            status="healthy",
            version="1.0.0",
            services={
                "openai": openai_status,
                "pinecone": pinecone_status,
                "s3": s3_status
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

