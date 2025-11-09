# RAGLedger Setup Guide

## Quick Start Checklist

Follow these steps to get RAGLedger up and running:

### 1. Prerequisites

- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed
- [ ] Docker and Docker Compose installed
- [ ] AWS CLI configured
- [ ] Terraform 1.5+ installed
- [ ] Git installed

### 2. AWS Account Setup

1. **Create AWS Account**
   - Sign up at https://aws.amazon.com/
   - Note: You provided AWS credentials (see README for security notes)

2. **Configure AWS CLI**
   ```bash
   aws configure
   # Use the provided credentials:
   # AWS Access Key ID: AKIAVD2QDXNTXMEHRGE2
   # AWS Secret Access Key: [provided]
   # Default region: us-east-1
   ```

3. **Create S3 Bucket for Terraform State** (One-time)
   ```bash
   aws s3 mb s3://ragledger-terraform-state
   aws s3api put-bucket-versioning \
     --bucket ragledger-terraform-state \
     --versioning-configuration Status=Enabled
   ```

### 3. API Keys Setup

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Create an API key
   - Add to `.env` file

2. **Pinecone API Key**
   - Sign up at https://www.pinecone.io/
   - Create an API key
   - Create an index:
     - Dimension: 3072
     - Metric: cosine
     - Region: us-east-1-aws
   - Add to `.env` file

### 4. Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd RAGLedger
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

4. **Start Services**
   ```bash
   # Option 1: Docker Compose (Recommended)
   docker-compose up -d
   
   # Option 2: Local Development
   # Terminal 1: Backend
   cd backend
   uvicorn main:app --reload
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### 5. Infrastructure Setup

1. **Initialize Terraform**
   ```bash
   cd infra/terraform
   terraform init
   ```

2. **Configure Terraform Variables**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

3. **Plan Infrastructure**
   ```bash
   terraform plan
   ```

4. **Apply Infrastructure** (Manual step - review carefully)
   ```bash
   terraform apply
   ```

5. **Store Secrets in AWS Secrets Manager**
   ```bash
   # OpenAI
   aws secretsmanager create-secret \
     --name ragledger/openai \
     --secret-string '{"api_key":"your-key","model":"gpt-4o-mini","embed_model":"text-embedding-3-large"}'
   
   # Pinecone
   aws secretsmanager create-secret \
     --name ragledger/pinecone \
     --secret-string '{"api_key":"your-key","environment":"us-east-1-aws","index":"ragledger"}'
   ```

### 6. Testing

1. **Test Backend**
   ```bash
   cd backend
   pytest tests/ -v
   ```

2. **Test Frontend**
   ```bash
   cd frontend
   npm test
   ```

3. **Test Ingestion**
   ```bash
   python scripts/ingest_local.py path/to/test.pdf
   ```

4. **Test Query**
   ```bash
   python scripts/test_query.py "What is the customer's credit limit?"
   ```

### 7. Deployment

See README.md for detailed deployment instructions.

## Troubleshooting

### Common Issues

1. **Pinecone Index Not Found**
   - Ensure index is created in Pinecone console
   - Check index name matches `PINECONE_INDEX` in `.env`

2. **AWS Credentials Error**
   - Verify AWS CLI is configured: `aws sts get-caller-identity`
   - Check IAM permissions

3. **OpenAI API Error**
   - Verify API key is correct
   - Check account has credits

4. **S3 Upload Error**
   - Verify S3 bucket exists
   - Check IAM permissions for S3 access

5. **Terraform State Error**
   - Ensure S3 bucket for state exists
   - Check DynamoDB table for state locking

## Next Steps

1. Upload a test document
2. Query the document
3. Explore the API documentation
4. Customize for your use case

## Support

For issues or questions, please open an issue on the repository.

