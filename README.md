# RAGLedger 🏦

<div align="center">

![RAGLedger Logo](https://img.shields.io/badge/RAGLedger-Banking%20RAG-blue?style=for-the-badge)

**A production-ready Retrieval-Augmented Generation (RAG) application for banking documents**

[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-430098?style=flat-square&logo=pinecone&logoColor=white)](https://www.pinecone.io/)
[![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Setup Guide](#setup-guide)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

RAGLedger is an end-to-end RAG application designed specifically for banking and financial documents. It enables users to upload PDF and CSV files, extract and index customer & credit-related information, and query the documents using AI-powered retrieval.

### Key Capabilities

- **Document Ingestion**: Upload and process PDF and CSV files
- **Intelligent Chunking**: Smart text chunking with metadata preservation
- **Vector Embeddings**: Generate embeddings using OpenAI's `text-embedding-3-large`
- **Semantic Search**: Retrieve relevant documents using Pinecone vector database
- **AI-Powered Answers**: Generate answers using GPT-4o-mini with source citations
- **Cloud-Native**: Fully deployed on AWS with Terraform infrastructure as code

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (React + TypeScript)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Upload     │  │   Ingest     │  │    Query     │         │
│  │   Router     │  │   Router     │  │   Router     │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                  │
│  ┌──────▼─────────────────▼──────────────────▼───────┐         │
│  │            Service Layer                          │         │
│  │  • OpenAI Service  • Pinecone Service            │         │
│  │  • Ingestion Service  • Query Service            │         │
│  └───────────────────────────────────────────────────┘         │
└─────────────┬──────────────┬──────────────┬────────────────────┘
              │              │              │
      ┌───────▼──────┐  ┌────▼────┐  ┌─────▼─────┐
      │     S3       │  │ Pinecone│  │  OpenAI   │
      │  (Documents) │  │(Vectors)│  │   API     │
      └──────────────┘  └─────────┘  └───────────┘
```

### Workflow Diagram

```
Upload → S3 Storage → Text Extraction → Chunking → Embedding → Pinecone
                                                                    │
Query → Embedding → Pinecone Search → Context Retrieval → GPT-4 → Answer
```

### Component Overview

1. **Frontend (React + TypeScript)**
   - File upload interface
   - Search interface
   - Results display with source citations
   - Built with Vite and TailwindCSS

2. **Backend (FastAPI)**
   - RESTful API endpoints
   - Document processing pipeline
   - Embedding generation
   - RAG query processing

3. **Vector Database (Pinecone)**
   - Stores document embeddings
   - Semantic search capabilities
   - Metadata filtering

4. **Cloud Infrastructure (AWS)**
   - S3 for document storage
   - Secrets Manager for API keys
   - EKS for containerized backend
   - CodeBuild/CodePipeline for CI/CD

---

## ✨ Features

### Document Processing
- ✅ PDF text extraction with page-level metadata
- ✅ CSV parsing with row-level indexing
- ✅ Intelligent chunking (500-1000 tokens) with overlap
- ✅ Metadata preservation (filename, page, customer_id, type)

### AI Capabilities
- ✅ OpenAI embeddings (`text-embedding-3-large`)
- ✅ GPT-4o-mini for answer generation
- ✅ Context-aware responses with source citations
- ✅ Similarity scoring for retrieved documents

### User Interface
- ✅ Modern, responsive design with TailwindCSS
- ✅ File upload with drag-and-drop support
- ✅ Real-time search interface
- ✅ Results display with source snippets and scores

### Infrastructure
- ✅ Terraform infrastructure as code
- ✅ AWS S3 for document storage
- ✅ AWS Secrets Manager for secure key management
- ✅ EKS for scalable backend deployment
- ✅ GitHub Actions CI/CD pipeline

### Security
- ✅ AWS Secrets Manager integration
- ✅ IAM roles and policies
- ✅ Encrypted S3 buckets
- ✅ Secure API key management

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **React Router** - Navigation

### Backend
- **Python 3.11** - Programming language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **PyPDF2** - PDF processing
- **Pandas** - CSV processing
- **Tiktoken** - Tokenization

### AI & ML
- **OpenAI API** - Embeddings and generation
- **Pinecone** - Vector database
- **text-embedding-3-large** - Embedding model
- **GPT-4o-mini** - Language model

### Infrastructure
- **AWS** - Cloud platform
  - S3 - Object storage
  - Secrets Manager - Secret management
  - EKS - Kubernetes
  - IAM - Access management
  - CodeBuild - CI/CD
- **Terraform** - Infrastructure as code
- **Docker** - Containerization
- **GitHub Actions** - Continuous integration

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** and Docker Compose
- **Terraform** 1.5+
- **AWS CLI** configured with credentials
- **Git** for version control

### AWS Account Setup

1. Create an AWS account
2. Configure AWS CLI:
   ```bash
   aws configure
   ```
3. Create IAM user with appropriate permissions
4. Set up S3 bucket for Terraform state (manual step)

### API Keys

You'll need:
- **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/)
- **Pinecone API Key** - Get from [Pinecone Console](https://app.pinecone.io/)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RAGLedger
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📖 Setup Guide

### Local Development Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### AWS Infrastructure Setup

#### 1. Initialize Terraform

```bash
cd infra/terraform
terraform init
```

#### 2. Create Terraform State Bucket (One-time)

```bash
aws s3 mb s3://ragledger-terraform-state
aws s3api put-bucket-versioning \
  --bucket ragledger-terraform-state \
  --versioning-configuration Status=Enabled
```

#### 3. Configure Terraform Variables

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

#### 4. Plan and Apply Infrastructure

```bash
terraform plan
terraform apply
```

#### 5. Store Secrets in AWS Secrets Manager

The Terraform configuration will create secrets in AWS Secrets Manager. You can also manually create them:

```bash
aws secretsmanager create-secret \
  --name ragledger/openai \
  --secret-string '{"api_key":"your-key","model":"gpt-4o-mini","embed_model":"text-embedding-3-large"}'

aws secretsmanager create-secret \
  --name ragledger/pinecone \
  --secret-string '{"api_key":"your-key","environment":"us-east-1-aws","index":"ragledger"}'
```

### Pinecone Setup

1. Create a Pinecone account at [pinecone.io](https://www.pinecone.io/)
2. Create an index with:
   - Dimension: 3072 (for text-embedding-3-large)
   - Metric: cosine
   - Region: us-east-1-aws (or your preferred region)

### CI/CD Setup

1. Configure GitHub Secrets:
   - Go to repository Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_ACCOUNT_ID`
     - `ECR_REGISTRY`
     - `ECR_REPOSITORY_BACKEND`
     - `ECR_REPOSITORY_FRONTEND`
     - `S3_BUCKET_FRONTEND`
     - `EKS_CLUSTER_NAME`
     - `OPENAI_API_KEY`
     - `PINECONE_API_KEY`

2. Push to GitHub to trigger workflow

---

## 🚢 Deployment

### Backend Deployment to EKS

1. Build and push Docker image:
   ```bash
   docker build -t ragledger-backend ./backend
   docker tag ragledger-backend:latest <ecr-repo>/ragledger-backend:latest
   docker push <ecr-repo>/ragledger-backend:latest
   ```

2. Deploy to EKS:
   ```bash
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl apply -f k8s/backend-service.yaml
   ```

### Frontend Deployment to S3

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy to S3:
   ```bash
   aws s3 sync dist/ s3://ragledger-frontend-dev/ --delete
   ```

### Using CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Tests frontend and backend
2. Builds Docker images
3. Pushes to ECR
4. Deploys to EKS (backend) and S3 (frontend)

---

## 📚 API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

#### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

Body: file (PDF or CSV)
```

#### Ingest Document
```http
POST /ingest
Content-Type: application/json

{
  "file_id": "uuid"
}
```

#### Query Documents
```http
POST /query
Content-Type: application/json

{
  "query": "What is the customer's credit limit?",
  "top_k": 5
}
```

### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI documentation.

---

## 🔒 Security

### Secrets Management

- **AWS Secrets Manager**: Stores OpenAI and Pinecone API keys
- **Environment Variables**: Used for local development
- **IAM Roles**: Application uses IAM roles for AWS service access

### Best Practices

1. Never commit API keys to version control
2. Use AWS Secrets Manager in production
3. Implement proper IAM policies
4. Enable S3 bucket encryption
5. Use HTTPS for all API communication
6. Implement rate limiting
7. Add authentication/authorization (TODO)

### Security Checklist

- [x] AWS Secrets Manager integration
- [x] Encrypted S3 buckets
- [x] IAM roles and policies
- [ ] API authentication (JWT/OAuth)
- [ ] Rate limiting
- [ ] Input validation and sanitization
- [ ] CORS configuration
- [ ] SSL/TLS certificates

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Manual Testing Scripts

```bash
# Test ingestion
python scripts/ingest_local.py path/to/document.pdf

# Test query
python scripts/test_query.py "What is the customer's credit limit?"
```

---

## 📝 Development Notes

### Project Structure

```
RAGLedger/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── utils/        # Utility functions
│   └── package.json
├── backend/               # FastAPI backend
│   ├── routers/          # API routes
│   ├── services/         # Business logic
│   ├── models/           # Pydantic models
│   └── requirements.txt
├── infra/                 # Infrastructure as code
│   └── terraform/        # Terraform configurations
├── scripts/               # Utility scripts
├── .github/workflows/    # GitHub Actions workflows
└── README.md
```

### Code Style

- **Python**: Black formatter, PEP 8
- **TypeScript**: ESLint, Prettier
- **Terraform**: Terraform fmt

### Logging

- Structured logging with Python's `logging` module
- Log levels: INFO, WARNING, ERROR
- CloudWatch integration (TODO)

---

## 🗺️ Roadmap

### Current Features
- ✅ Document upload and ingestion
- ✅ Vector embedding generation
- ✅ Semantic search
- ✅ AI-powered question answering
- ✅ Basic UI

### Planned Features
- [ ] User authentication and authorization
- [ ] Multi-tenant support
- [ ] Advanced filtering and search
- [ ] Document versioning
- [ ] Real-time collaboration
- [ ] Analytics dashboard
- [ ] Export functionality
- [ ] API rate limiting
- [ ] Webhook support
- [ ] GraphQL API

### Future Enhancements
- [ ] Support for more file formats (Word, Excel)
- [ ] OCR for scanned documents
- [ ] Multi-language support
- [ ] Advanced chunking strategies
- [ ] Fine-tuned models
- [ ] Caching layer (Redis)
- [ ] Message queue (SQS/RabbitMQ)
- [ ] Monitoring and alerting (CloudWatch, Datadog)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style
- Write tests for new features
- Update documentation
- Ensure all tests pass
- Follow semantic versioning

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for powerful language models
- **Pinecone** for vector database infrastructure
- **AWS** for cloud platform
- **FastAPI** for excellent Python web framework
- **React** for UI framework

---

## 📞 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

## 🎉 Getting Started Checklist

- [ ] Clone the repository
- [ ] Set up AWS account and configure CLI
- [ ] Create OpenAI API key
- [ ] Create Pinecone account and index
- [ ] Configure environment variables
- [ ] Set up Terraform state bucket
- [ ] Run `terraform init` and `terraform apply`
- [ ] Store secrets in AWS Secrets Manager
- [ ] Install dependencies (`npm install`, `pip install -r requirements.txt`)
- [ ] Start backend (`uvicorn main:app --reload`)
- [ ] Start frontend (`npm run dev`)
- [ ] Upload a test document
- [ ] Query the document

---

<div align="center">

**Built with ❤️ for banking and financial document processing**

[RAGLedger](https://github.com/your-org/ragledger) • [Documentation](#) • [Issues](#)

</div>

