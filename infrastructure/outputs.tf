output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.frontend_bucket.id
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
  value       = aws_dynamodb_table.lottery_data.name
}

output "api_endpoint" {
  description = "The URL of the API Gateway"
  value       = "${aws_apigatewayv2_api.http_api.api_endpoint}/check"
}