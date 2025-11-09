#!/usr/bin/env python3
"""
Local ingestion script for testing document ingestion
"""

import asyncio
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.ingestion_service import IngestionService
from services.openai_service import OpenAIService
from services.pinecone_service import PineconeService
import boto3
from botocore.exceptions import ClientError


async def ingest_local_file(file_path: str, file_id: str = None):
    """
    Ingest a local file for testing
    """
    if file_id is None:
        import uuid
        file_id = str(uuid.uuid4())
    
    # Upload to S3 first (for testing)
    s3_client = boto3.client('s3')
    s3_bucket = os.getenv('S3_BUCKET', 'ragledger-documents-dev')
    s3_key = f"documents/{file_id}/{os.path.basename(file_path)}"
    
    try:
        print(f"Uploading {file_path} to S3...")
        s3_client.upload_file(file_path, s3_bucket, s3_key)
        print(f"Uploaded to S3: s3://{s3_bucket}/{s3_key}")
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return
    
    # Ingest the document
    try:
        ingestion_service = IngestionService()
        result = await ingestion_service.ingest_document(file_id)
        print(f"Ingestion complete!")
        print(f"  File ID: {result['file_id']}")
        print(f"  Filename: {result['filename']}")
        print(f"  Chunks processed: {result['chunks_processed']}")
    except Exception as e:
        print(f"Error ingesting document: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(description='Ingest a local file')
    parser.add_argument('file_path', help='Path to the file to ingest')
    parser.add_argument('--file-id', help='File ID (optional)', default=None)
    parser.add_argument('--s3-bucket', help='S3 bucket name', default=None)
    
    args = parser.parse_args()
    
    if args.s3_bucket:
        os.environ['S3_BUCKET'] = args.s3_bucket
    
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        sys.exit(1)
    
    asyncio.run(ingest_local_file(args.file_path, args.file_id))


if __name__ == "__main__":
    main()

