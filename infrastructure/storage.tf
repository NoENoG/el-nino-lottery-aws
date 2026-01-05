# --- DYNAMODB ---
resource "aws_dynamodb_table" "lottery_data" {
  name         = "${var.project_name}-results"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "DrawDate"
  attribute {
    name = "DrawDate"
    type = "S"
  }
}

# --- S3 BUCKET ---
resource "aws_s3_bucket" "frontend_bucket" {
  bucket        = "${var.project_name}-frontend"
  force_destroy = false # Set to false to protect your data
}

# --- S3 BLOCK PUBLIC ACCESS ---
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.frontend_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- FILE UPLOADS ---
resource "aws_s3_object" "site_files" {
  for_each     = fileset("${path.module}/frontend", "**/*")
  bucket       = aws_s3_bucket.frontend_bucket.id
  key          = each.value
  source       = "${path.module}/frontend/${each.value}"
  etag         = filemd5("${path.module}/frontend/${each.value}") 
  content_type = lookup({
    "html" = "text/html", "css" = "text/css", "js" = "application/javascript"
  }, split(".", each.value)[length(split(".", each.value)) - 1], "text/plain")
}