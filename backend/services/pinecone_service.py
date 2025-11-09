"""
Pinecone Service - handles vector database operations
"""

import os
import logging
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class PineconeService:
    """
    Service for Pinecone vector database operations
    """
    
    def __init__(self):
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = os.getenv('PINECONE_INDEX', 'ragledger')
        
        # Initialize or connect to index
        try:
            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                logger.info(f"Index {self.index_name} does not exist. Creating...")
                self._create_index()
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {e}")
            raise
    
    def _create_index(self):
        """
        Create a new Pinecone index if it doesn't exist
        """
        try:
            self.pc.create_index(
                name=self.index_name,
                dimension=3072,  # text-embedding-3-large dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            logger.info(f"Created Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            raise
    
    async def upsert_vectors(
        self,
        vectors: List[List[float]],
        ids: List[str],
        metadata: List[Dict[str, Any]]
    ):
        """
        Upsert vectors into Pinecone
        """
        try:
            # Prepare vectors for upsert
            vectors_to_upsert = [
                {
                    "id": ids[i],
                    "values": vectors[i],
                    "metadata": metadata[i]
                }
                for i in range(len(vectors))
            ]
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Upserted {len(vectors_to_upsert)} vectors to Pinecone")
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise
    
    async def query_vectors(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query vectors from Pinecone
        """
        try:
            query_response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                filter=filter
            )
            
            results = []
            for match in query_response.matches:
                results.append({
                    'id': match.id,
                    'score': match.score,
                    'metadata': match.metadata
                })
            
            return results
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            raise

