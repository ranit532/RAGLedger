"""
Upload router - handles file uploads
"""

import logging
import uuid
import boto3
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import UploadResponse
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize S3 client
s3_client = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET', 'ragledger-documents')


@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or CSV file to S3
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['pdf', 'csv']:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and CSV files are supported"
            )

        # Generate unique file ID
        file_id = str(uuid.uuid4())
        s3_key = f"documents/{file_id}/{file.filename}"

        # Read file content
        file_content = await file.read()

        # Upload to S3
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=file_content,
                ContentType=file.content_type or f"application/{file_ext}",
                Metadata={
                    'original_filename': file.filename,
                    'file_id': file_id,
                    'file_type': file_ext
                }
            )
            logger.info(f"File uploaded to S3: {s3_key}")
        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to S3: {str(e)}"
            )

        return UploadResponse(
            message="File uploaded successfully",
            file_id=file_id,
            filename=file.filename
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

