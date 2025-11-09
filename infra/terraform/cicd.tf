# CodeBuild project for CI/CD
resource "aws_codebuild_project" "ragledger" {
  name          = "${var.project_name}-build-${var.environment}"
  description   = "Build project for RAGLedger"
  build_timeout = 60
  service_role  = aws_iam_role.cicd_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = var.aws_region
    }

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "ECR_REPOSITORY_BACKEND"
      value = aws_ecr_repository.backend.name
    }

    environment_variable {
      name  = "ECR_REPOSITORY_FRONTEND"
      value = aws_ecr_repository.frontend.name
    }

    environment_variable {
      name  = "S3_BUCKET_FRONTEND"
      value = aws_s3_bucket.frontend.id
    }
  }

  source {
    type            = "GITLAB"
    location        = var.gitlab_repo_url
    git_clone_depth = 1
  }

  tags = {
    Name = "${var.project_name}-build-${var.environment}"
  }
}

data "aws_caller_identity" "current" {}

variable "gitlab_repo_url" {
  description = "GitLab repository URL"
  type        = string
  default     = ""
}

# CodePipeline (optional - can be set up separately)
# This is a basic structure - you may want to customize based on your needs

