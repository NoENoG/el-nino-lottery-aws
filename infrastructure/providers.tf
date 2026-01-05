provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ElNino2026"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}