locals {
  name_prefix = "${var.project_name}-${var.environment}"

  lambda_function_name = "${local.name_prefix}-generate-plan"
  api_name             = "${local.name_prefix}-http-api"
  amplify_name         = var.amplify_app_name != "" ? var.amplify_app_name : local.name_prefix

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Application = "FocusFlowAI"
  }

  # Nova may be invoked via foundation-model or inference-profile ARNs depending on region/account setup.
  bedrock_foundation_model_arn  = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.bedrock_model_id}"
  bedrock_inference_profile_arn = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:inference-profile/*"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
