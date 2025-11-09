output "s3_bucket_documents" {
  description = "S3 bucket for documents"
  value       = aws_s3_bucket.documents.id
}

output "s3_bucket_frontend" {
  description = "S3 bucket for frontend"
  value       = aws_s3_bucket.frontend.id
}

output "s3_bucket_frontend_website_url" {
  description = "S3 website URL for frontend"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "dynamodb_table_terraform_locks" {
  description = "DynamoDB table for Terraform state locking"
  value       = aws_dynamodb_table.terraform_locks.id
}

output "secrets_manager_openai_arn" {
  description = "ARN of OpenAI secret in Secrets Manager"
  value       = aws_secretsmanager_secret.openai.arn
}

output "secrets_manager_pinecone_arn" {
  description = "ARN of Pinecone secret in Secrets Manager"
  value       = aws_secretsmanager_secret.pinecone.arn
}

output "iam_role_app_arn" {
  description = "ARN of application IAM role"
  value       = aws_iam_role.app_role.arn
}

output "iam_role_cicd_arn" {
  description = "ARN of CI/CD IAM role"
  value       = aws_iam_role.cicd_role.arn
}

output "eks_cluster_name" {
  description = "Name of EKS cluster"
  value       = aws_eks_cluster.ragledger.name
}

output "eks_cluster_endpoint" {
  description = "Endpoint of EKS cluster"
  value       = aws_eks_cluster.ragledger.endpoint
}

output "ecr_repository_backend_url" {
  description = "URL of ECR repository for backend"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_repository_frontend_url" {
  description = "URL of ECR repository for frontend"
  value       = aws_ecr_repository.frontend.repository_url
}

output "codebuild_project_name" {
  description = "Name of CodeBuild project"
  value       = aws_codebuild_project.ragledger.name
}

