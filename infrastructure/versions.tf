terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }


backend "s3" {
    bucket = "el-nino-2026-aws-frontend"
    key    = "el-nino/terraform.tfstate"
    region = "eu-west-1"
  }
  }