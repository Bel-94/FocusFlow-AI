data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../backend"
  output_path = "${path.module}/build/lambda.zip"
  excludes = [
    "__pycache__",
    "*.pyc",
    ".gitkeep",
    "requirements.txt",
    "tests",
    ".pytest_cache",
  ]
}

resource "aws_lambda_function" "api" {
  function_name = local.lambda_function_name
  description   = "FocusFlow AI API handler — generate plans via Bedrock and manage history."
  role          = aws_iam_role.lambda.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  architectures = ["x86_64"]

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout

  environment {
    variables = {
      TABLE_NAME       = aws_dynamodb_table.focus_plans.name
      BEDROCK_MODEL_ID = var.bedrock_model_id
      HISTORY_LIMIT    = tostring(var.history_limit)
      MAX_TASKS_CHARS  = tostring(var.max_tasks_chars)
      LOG_LEVEL        = "INFO"
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy.lambda,
  ]

  tags = {
    Name = local.lambda_function_name
  }
}

resource "aws_lambda_permission" "allow_apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
