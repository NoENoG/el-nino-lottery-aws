terraform {
  backend "s3" {
    bucket = "el-nino-terraform-state-backend"
    key    = "el-nino/terraform.tfstate"
    region = "eu-west-1"
  }
}