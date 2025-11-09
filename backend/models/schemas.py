"""
Pydantic models for request/response schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class UploadResponse(BaseModel):
    message: str
    file_id: str
    filename: str


class IngestRequest(BaseModel):
    file_id: str


class IngestResponse(BaseModel):
    message: str
    chunks_processed: int


class QueryRequest(BaseModel):
    query: str = Field(..., description="The question to ask")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to retrieve")


class Source(BaseModel):
    filename: str
    page: Optional[int] = None
    chunk_id: str
    similarity_score: float
    content: str
    metadata: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    query: str


class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]

