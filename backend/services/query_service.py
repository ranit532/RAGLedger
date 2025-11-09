"""
Query Service - handles RAG queries
"""

import logging
from typing import List, Dict, Any
from services.openai_service import OpenAIService
from services.pinecone_service import PineconeService
from models.schemas import Source

logger = logging.getLogger(__name__)


class QueryService:
    """
    Service for processing RAG queries
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.pinecone_service = PineconeService()
    
    async def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a query: embed, retrieve, and generate answer
        """
        try:
            # Generate query embedding
            query_embeddings = await self.openai_service.generate_embeddings([query])
            query_vector = query_embeddings[0]
            
            # Query Pinecone
            results = await self.pinecone_service.query_vectors(
                query_vector=query_vector,
                top_k=top_k
            )
            
            # Extract context and sources
            context = []
            sources = []
            
            for result in results:
                metadata = result['metadata']
                content = metadata.get('content', '')
                
                # Get full content if available (you might want to store this differently)
                # For now, we'll use the stored content snippet
                context.append(content)
                
                sources.append(Source(
                    filename=metadata.get('filename', 'unknown'),
                    page=metadata.get('page'),
                    chunk_id=result['id'],
                    similarity_score=result['score'],
                    content=content,
                    metadata={
                        'file_id': metadata.get('file_id'),
                        'type': metadata.get('type')
                    }
                ))
            
            # Generate answer using retrieved context
            if context:
                answer = await self.openai_service.generate_answer(query, context)
            else:
                answer = "I couldn't find any relevant information in the documents to answer your question."
            
            return {
                'answer': answer,
                'sources': sources,
                'query': query
            }
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            raise

