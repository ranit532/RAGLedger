"""
Secrets Service - manages AWS Secrets Manager integration
"""

import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SecretsService:
    """
    Service for fetching secrets from AWS Secrets Manager
    Falls back to environment variables for local development
    """
    
    def __init__(self):
        self.secrets_client = None
        self.secrets_loaded = False
        
        # Try to initialize AWS client
        try:
            self.secrets_client = boto3.client('secretsmanager')
        except Exception as e:
            logger.warning(f"Could not initialize Secrets Manager client: {e}")
            logger.info("Falling back to environment variables")
    
    async def load_secrets(self):
        """
        Load secrets from AWS Secrets Manager
        """
        if not self.secrets_client:
            logger.info("Using environment variables for secrets")
            return
        
        try:
            # Load OpenAI secrets
            openai_secrets = self._get_secret('ragledger/openai')
            if openai_secrets:
                os.environ['OPENAI_API_KEY'] = openai_secrets.get('api_key', os.getenv('OPENAI_API_KEY', ''))
                os.environ['OPENAI_MODEL'] = openai_secrets.get('model', os.getenv('OPENAI_MODEL', 'gpt-4o-mini'))
                os.environ['OPENAI_EMBED_MODEL'] = openai_secrets.get('embed_model', os.getenv('OPENAI_EMBED_MODEL', 'text-embedding-3-large'))
            
            # Load Pinecone secrets
            pinecone_secrets = self._get_secret('ragledger/pinecone')
            if pinecone_secrets:
                os.environ['PINECONE_API_KEY'] = pinecone_secrets.get('api_key', os.getenv('PINECONE_API_KEY', ''))
                os.environ['PINECONE_ENVIRONMENT'] = pinecone_secrets.get('environment', os.getenv('PINECONE_ENVIRONMENT', ''))
                os.environ['PINECONE_INDEX'] = pinecone_secrets.get('index', os.getenv('PINECONE_INDEX', 'ragledger'))
            
            self.secrets_loaded = True
            logger.info("Secrets loaded from AWS Secrets Manager")
        except Exception as e:
            logger.warning(f"Failed to load secrets from AWS: {e}")
            logger.info("Using environment variables instead")
    
    def _get_secret(self, secret_name: str) -> dict:
        """
        Retrieve a secret from AWS Secrets Manager
        """
        if not self.secrets_client:
            return None
        
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            secret_string = response['SecretString']
            return json.loads(secret_string)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.warning(f"Secret {secret_name} not found in Secrets Manager")
            else:
                logger.error(f"Error retrieving secret {secret_name}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing secret {secret_name}: {e}")
            return None

