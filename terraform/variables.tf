variable "aws_region" {
  description = "AWS region for all resources. Choose a region where Amazon Bedrock Nova Lite is available."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming and tags."
  type        = string
  default     = "focusflow-ai"
}

variable "environment" {
  description = "Deployment environment label (e.g. challenge, dev, prod)."
  type        = string
  default     = "challenge"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name for stored plans."
  type        = string
  default     = "FocusPlans"
}

variable "bedrock_model_id" {
  description = "Amazon Bedrock foundation model ID used for plan generation."
  type        = string
  default     = "amazon.nova-lite-v1:0"
}

variable "lambda_memory_size" {
  description = "Lambda memory in MB."
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds. Bedrock calls need headroom."
  type        = number
  default     = 30
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention for the Lambda log group."
  type        = number
  default     = 14
}

variable "cors_allow_origins" {
  description = "Allowed CORS origins for the HTTP API. Use [\"*\"] for challenge demos; tighten to the Amplify URL in production."
  type        = list(string)
  default     = ["*"]
}

variable "api_stage_name" {
  description = "API Gateway HTTP API stage name."
  type        = string
  default     = "$default"
}

variable "history_limit" {
  description = "Max number of history items returned by GET /history."
  type        = number
  default     = 20
}

variable "max_tasks_chars" {
  description = "Maximum allowed characters for the tasks input field."
  type        = number
  default     = 4000
}

variable "amplify_app_name" {
  description = "Display name for the Amplify application. Defaults to project-environment when empty."
  type        = string
  default     = ""
}

variable "amplify_repository_url" {
  description = "Optional GitHub repository URL for Amplify. Leave empty to create the app shell and connect the repo in the console."
  type        = string
  default     = ""
}

variable "amplify_access_token" {
  description = "Optional GitHub personal access token for Amplify repo connection. Leave empty when connecting manually."
  type        = string
  default     = ""
  sensitive   = true
}

variable "amplify_branch_name" {
  description = "Git branch Amplify should build when a repository is connected."
  type        = string
  default     = "main"
}

variable "amplify_enable_branch" {
  description = "Whether to create an Amplify branch resource. Set false until a repository is connected."
  type        = bool
  default     = false
}
