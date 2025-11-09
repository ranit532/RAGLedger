"""
OpenAI Service - handles OpenAI API interactions
"""

import os
import logging
from openai import OpenAI
from typing import List

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Service for OpenAI API interactions
    Handles embeddings and chat completions
    """
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.embed_model = os.getenv('OPENAI_EMBED_MODEL', 'text-embedding-3-large')
        
        logger.info(f"OpenAI service initialized with model: {self.model}, embed_model: {self.embed_model}")
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        """
        try:
            response = self.client.embeddings.create(
                model=self.embed_model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    async def generate_answer(self, query: str, context: List[str]) -> str:
        """
        Generate an answer using GPT model with retrieved context
        """
        try:
            # Construct prompt with context
            context_text = "\n\n".join([
                f"[Document {i+1}]\n{ctx}" for i, ctx in enumerate(context)
            ])
            
            prompt = f"""You are a helpful assistant that answers questions based on the provided banking documents.

Context from documents:
{context_text}

Question: {query}

Please provide a comprehensive answer based on the context above. If the context doesn't contain enough information to answer the question, please say so.

Answer:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about banking documents. Always cite your sources when providing information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

