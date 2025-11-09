"""
RAGLedger Backend - FastAPI Application
Main entry point for the RAG application
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import upload, ingest, query, health
from services.secrets_service import SecretsService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting RAGLedger backend...")
    try:
        # Initialize secrets service and load secrets
        secrets_service = SecretsService()
        await secrets_service.load_secrets()
        logger.info("Secrets loaded successfully")
    except Exception as e:
        logger.error(f"Error loading secrets: {e}")
        logger.warning("Continuing with environment variables...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAGLedger backend...")


# Create FastAPI app
app = FastAPI(
    title="RAGLedger API",
    description="Retrieval-Augmented Generation API for Banking Documents",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(query.router, prefix="/query", tags=["query"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

