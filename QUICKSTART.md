# RAGLedger Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Prerequisites
```bash
# Check installations
node --version  # Should be 18+
python --version  # Should be 3.11+
docker --version
terraform --version
```

### Step 2: Clone and Setup
```bash
git clone <repository-url>
cd RAGLedger
cp .env.example .env
# Edit .env with your API keys (OpenAI, Pinecone, AWS)
```

### Step 3: Start with Docker (Easiest)
```bash
docker-compose up -d
```

### Step 4: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 5: Test the Application
1. Go to http://localhost:3000
2. Upload a PDF or CSV file
3. Wait for ingestion to complete
4. Go to Query page
5. Ask a question about your document

## 📋 What You Need

### API Keys
- **OpenAI API Key**: Get from https://platform.openai.com/
- **Pinecone API Key**: Get from https://www.pinecone.io/
- **AWS Credentials**: Configure with `aws configure`

### Pinecone Setup
1. Create account at https://www.pinecone.io/
2. Create index:
   - Name: `ragledger`
   - Dimension: `3072`
   - Metric: `cosine`
   - Region: `us-east-1-aws`

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

## 🧪 Test Scripts

```bash
# Test ingestion
python scripts/ingest_local.py path/to/document.pdf

# Test query
python scripts/test_query.py "What is the customer's credit limit?"
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

### API Key Errors
- Check `.env` file has correct keys
- Verify keys are valid in respective platforms
- Check environment variables are loaded

### S3 Errors
- Ensure AWS credentials are configured
- Check S3 bucket exists (or create manually)
- Verify IAM permissions

## 📚 Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Check [SETUP.md](SETUP.md) for infrastructure setup
3. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture

## 💡 Tips

- Use Docker for easiest setup
- Check API docs at `/docs` endpoint
- Monitor logs with `docker-compose logs -f`
- Test with small documents first
- Use health endpoint to verify services

## 🎉 You're Ready!

Your RAGLedger application is now running. Start uploading documents and querying them!

