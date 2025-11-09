"""
Ingestion Service - handles document processing and ingestion
"""

import os
import logging
import uuid
import boto3
import pandas as pd
from PyPDF2 import PdfReader
from typing import List, Dict, Any
from services.openai_service import OpenAIService
from services.pinecone_service import PineconeService
import tiktoken

logger = logging.getLogger(__name__)

# Initialize services
s3_client = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET', 'ragledger-documents')

# Tokenizer for chunking
encoding = tiktoken.get_encoding("cl100k_base")


class IngestionService:
    """
    Service for ingesting documents: extract, chunk, embed, and store
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.pinecone_service = PineconeService()
        self.chunk_size = 500  # tokens
        self.chunk_overlap = 50  # tokens
    
    async def ingest_document(self, file_id: str) -> Dict[str, Any]:
        """
        Ingest a document: download from S3, extract text, chunk, embed, and store
        """
        try:
            # Download file from S3
            file_info = await self._download_file(file_id)
            filename = file_info['filename']
            file_path = file_info['local_path']
            file_type = file_info['file_type']
            
            # Extract text based on file type
            if file_type == 'pdf':
                chunks = await self._extract_pdf_text(file_path, filename)
            elif file_type == 'csv':
                chunks = await self._extract_csv_text(file_path, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Generate embeddings
            texts = [chunk['content'] for chunk in chunks]
            embeddings = await self.openai_service.generate_embeddings(texts)
            
            # Prepare vectors for Pinecone
            vector_ids = [f"{file_id}_{i}" for i in range(len(chunks))]
            metadata_list = [
                {
                    'filename': chunk['filename'],
                    'chunk_id': vector_ids[i],
                    'file_id': file_id,
                    'page': chunk.get('page'),
                    'type': file_type,
                    'content': chunk['content'][:500]  # Store first 500 chars for display
                }
                for i, chunk in enumerate(chunks)
            ]
            
            # Upsert to Pinecone
            await self.pinecone_service.upsert_vectors(
                vectors=embeddings,
                ids=vector_ids,
                metadata=metadata_list
            )
            
            # Cleanup local file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            logger.info(f"Ingested {len(chunks)} chunks for file {filename}")
            
            return {
                'chunks_processed': len(chunks),
                'file_id': file_id,
                'filename': filename
            }
        except Exception as e:
            logger.error(f"Error ingesting document: {e}", exc_info=True)
            raise
    
    async def _download_file(self, file_id: str) -> Dict[str, Any]:
        """
        Download file from S3 to local temporary storage
        """
        try:
            # List objects with prefix to find the file
            response = s3_client.list_objects_v2(
                Bucket=S3_BUCKET,
                Prefix=f"documents/{file_id}/"
            )
            
            if 'Contents' not in response or len(response['Contents']) == 0:
                raise FileNotFoundError(f"File not found in S3: {file_id}")
            
            # Get the first file (should be only one)
            s3_key = response['Contents'][0]['Key']
            filename = os.path.basename(s3_key)
            
            # Download to temporary location
            local_path = f"/tmp/{file_id}_{filename}"
            s3_client.download_file(S3_BUCKET, s3_key, local_path)
            
            # Get file type
            file_type = filename.split('.')[-1].lower()
            
            return {
                'filename': filename,
                'local_path': local_path,
                'file_type': file_type,
                's3_key': s3_key
            }
        except Exception as e:
            logger.error(f"Error downloading file from S3: {e}")
            raise
    
    async def _extract_pdf_text(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF and chunk it
        """
        try:
            reader = PdfReader(file_path)
            chunks = []
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text.strip():
                    continue
                
                # Chunk the text
                page_chunks = self._chunk_text(text, filename, page_num + 1)
                chunks.extend(page_chunks)
            
            return chunks
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise
    
    async def _extract_csv_text(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """
        Extract text from CSV and chunk it
        """
        try:
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to text representation
            text_parts = []
            for idx, row in df.iterrows():
                row_text = f"Row {idx + 1}:\n"
                for col, val in row.items():
                    row_text += f"{col}: {val}\n"
                text_parts.append(row_text)
            
            full_text = "\n\n".join(text_parts)
            chunks = self._chunk_text(full_text, filename)
            
            return chunks
        except Exception as e:
            logger.error(f"Error extracting CSV text: {e}")
            raise
    
    def _chunk_text(self, text: str, filename: str, page: int = None) -> List[Dict[str, Any]]:
        """
        Chunk text into smaller pieces with overlap
        """
        # Tokenize text
        tokens = encoding.encode(text)
        
        chunks = []
        start = 0
        
        while start < len(tokens):
            # Get chunk
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens)
            
            chunks.append({
                'content': chunk_text,
                'filename': filename,
                'page': page
            })
            
            # Move start position with overlap
            start = end - self.chunk_overlap
        
        return chunks

