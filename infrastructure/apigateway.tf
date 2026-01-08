resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS", "GET"]
    allow_headers = ["content-type", "authorization", "x-amz-date", "x-api-key"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "reader_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.reader.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_check" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /check"
  target    = "integrations/${aws_apigatewayv2_integration.reader_integration.id}"
}

resource "aws_lambda_permission" "api_gw_reader" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reader.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*/check"
}