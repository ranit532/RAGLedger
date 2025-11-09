# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD.

## Workflows

### `ci-cd.yml`
Main CI/CD pipeline that:
- Tests frontend and backend
- Builds Docker images
- Pushes to ECR
- Plans and applies Terraform
- Deploys to S3 (frontend) and EKS (backend)

## Required Secrets

Configure these secrets in GitHub (Settings → Secrets and variables → Actions):

- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `ECR_REGISTRY` - ECR registry URL
- `ECR_REPOSITORY_BACKEND` - ECR repository name for backend
- `ECR_REPOSITORY_FRONTEND` - ECR repository name for frontend
- `S3_BUCKET_FRONTEND` - S3 bucket name for frontend
- `EKS_CLUSTER_NAME` - EKS cluster name
- `OPENAI_API_KEY` - OpenAI API key (for Terraform)
- `PINECONE_API_KEY` - Pinecone API key (for Terraform)
- `CLOUDFRONT_DISTRIBUTION_ID` - (Optional) CloudFront distribution ID

## OIDC Authentication (Recommended)

For better security, use OIDC authentication instead of access keys:

1. Create OIDC provider in AWS IAM:
   ```bash
   aws iam create-open-id-connect-provider \
     --url https://token.actions.githubusercontent.com \
     --client-id-list sts.amazonaws.com \
     --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
   ```

2. Update the workflow to use OIDC (see workflow file comments)

3. The Terraform configuration includes IAM role for GitHub Actions OIDC

## Workflow Triggers

- **Push to main/develop**: Runs full CI/CD pipeline
- **Pull Request**: Runs tests and Terraform plan only

