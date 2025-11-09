# AWS Secrets Manager - OpenAI secrets
resource "aws_secretsmanager_secret" "openai" {
  name        = "ragledger/openai"
  description = "OpenAI API credentials for RAGLedger"

  tags = {
    Name = "${var.project_name}-openai-secret"
  }
}

resource "aws_secretsmanager_secret_version" "openai" {
  secret_id = aws_secretsmanager_secret.openai.id
  secret_string = jsonencode({
    api_key     = var.openai_api_key
    model       = var.openai_model
    embed_model = var.openai_embed_model
  })
}

# AWS Secrets Manager - Pinecone secrets
resource "aws_secretsmanager_secret" "pinecone" {
  name        = "ragledger/pinecone"
  description = "Pinecone API credentials for RAGLedger"

  tags = {
    Name = "${var.project_name}-pinecone-secret"
  }
}

resource "aws_secretsmanager_secret_version" "pinecone" {
  secret_id = aws_secretsmanager_secret.pinecone.id
  secret_string = jsonencode({
    api_key    = var.pinecone_api_key
    environment = var.pinecone_environment
    index      = var.pinecone_index
  })
}

# Variables for secrets (should be provided via terraform.tfvars or environment variables)
variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "openai_model" {
  description = "OpenAI model name"
  type        = string
  default     = "gpt-4o-mini"
}

variable "openai_embed_model" {
  description = "OpenAI embedding model name"
  type        = string
  default     = "text-embedding-3-large"
}

variable "pinecone_api_key" {
  description = "Pinecone API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "pinecone_environment" {
  description = "Pinecone environment"
  type        = string
  default     = "us-east-1-aws"
}

variable "pinecone_index" {
  description = "Pinecone index name"
  type        = string
  default     = "ragledger"
}

