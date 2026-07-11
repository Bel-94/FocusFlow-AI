output "aws_region" {
  description = "AWS region where resources were deployed."
  value       = var.aws_region
}

output "api_endpoint" {
  description = "Base URL of the API Gateway HTTP API (no trailing slash)."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "generate_plan_url" {
  description = "Full URL for POST /generate-plan."
  value       = "${aws_apigatewayv2_api.http.api_endpoint}/generate-plan"
}

output "history_url" {
  description = "Full URL for GET /history."
  value       = "${aws_apigatewayv2_api.http.api_endpoint}/history"
}

output "lambda_function_name" {
  description = "Name of the API Lambda function."
  value       = aws_lambda_function.api.function_name
}

output "lambda_function_arn" {
  description = "ARN of the API Lambda function."
  value       = aws_lambda_function.api.arn
}

output "dynamodb_table_name" {
  description = "DynamoDB table storing generated plans."
  value       = aws_dynamodb_table.focus_plans.name
}

output "dynamodb_table_arn" {
  description = "ARN of the FocusPlans table."
  value       = aws_dynamodb_table.focus_plans.arn
}

output "lambda_log_group" {
  description = "CloudWatch Log Group for Lambda."
  value       = aws_cloudwatch_log_group.lambda.name
}

output "api_access_log_group" {
  description = "CloudWatch Log Group for API Gateway access logs."
  value       = aws_cloudwatch_log_group.api_gateway.name
}

output "bedrock_model_id" {
  description = "Bedrock model ID configured for the Lambda."
  value       = var.bedrock_model_id
}

output "amplify_app_id" {
  description = "Amplify application ID."
  value       = aws_amplify_app.frontend.id
}

output "amplify_app_name" {
  description = "Amplify application name."
  value       = aws_amplify_app.frontend.name
}

output "amplify_default_domain" {
  description = "Amplify default domain (branch URL appears after a branch is connected and built)."
  value       = aws_amplify_app.frontend.default_domain
}

output "frontend_api_base_url_hint" {
  description = "Value to set as API_BASE_URL for the Streamlit frontend."
  value       = aws_apigatewayv2_api.http.api_endpoint
}
