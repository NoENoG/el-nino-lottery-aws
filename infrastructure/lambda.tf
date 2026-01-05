 data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/scraper.py"
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "scraper" {
  filename         = "lambda_function.zip"
  function_name    = "${var.project_name}-scraper"
  role             = aws_iam_role.scraper_role.arn
  handler          = "scraper.lambda_handler"
  runtime          = "python3.12"
  timeout          = 300
  memory_size      = 512
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  
  environment { 
    variables = { 
        DYNAMODB_TABLE = aws_dynamodb_table.lottery_data.name 
    } 
  }
}

# --- INGESTER LAMBDA ---
data "archive_file" "ingester_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/ingester.py"
  output_path = "ingester_function.zip"
}

resource "aws_lambda_function" "ingester" {
  filename         = "ingester_function.zip"
  function_name    = "${var.project_name}-ingester"
  role             = aws_iam_role.scraper_role.arn
  handler          = "ingester.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  source_code_hash = data.archive_file.ingester_zip.output_base64sha256
  
  environment { 
    variables = { 
        DYNAMODB_TABLE = aws_dynamodb_table.lottery_data.name 
    } 
  }
}
# --- READER LAMBDA ---
data "archive_file" "reader_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/reader.py"
  output_path = "reader_function.zip"
}

resource "aws_lambda_function" "reader" {
  filename         = "reader_function.zip"
  function_name    = "${var.project_name}-reader"
  role             = aws_iam_role.scraper_role.arn # Reusing the role is fine for now
  handler          = "reader.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.reader_zip.output_base64sha256
  
  environment { 
    variables = { 
        DYNAMODB_TABLE = aws_dynamodb_table.lottery_data.name 
    } 
  }
}