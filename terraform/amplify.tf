# Amplify Hosting for the Streamlit frontend.
#
# Streamlit requires a runtime (Docker), not static hosting.
# This resource creates the Amplify app shell and injects API_BASE_URL.
# Connect the GitHub repo + Dockerfile build in the console if
# amplify_repository_url / amplify_access_token are left empty.
# See docs/amplify-deploy.md.

resource "aws_amplify_app" "frontend" {
  name        = local.amplify_name
  description = "FocusFlow AI Streamlit frontend"
  platform    = "WEB"

  repository   = var.amplify_repository_url != "" ? var.amplify_repository_url : null
  access_token = var.amplify_access_token != "" ? var.amplify_access_token : null

  environment_variables = {
    API_BASE_URL = aws_apigatewayv2_api.http.api_endpoint
    # Streamlit reads this at runtime when deployed via Docker / compute hosting.
  }

  # Placeholder build spec for when a repo is connected.
  # Replace/adjust after Dockerfile-based hosting is confirmed in the Amplify console.
  build_spec = <<-EOT
    version: 1
    frontend:
      phases:
        preBuild:
          commands:
            - echo "FocusFlow AI Amplify build — prefer Dockerfile-based hosting for Streamlit"
            - cd frontend || true
            - pip install -r requirements.txt || true
        build:
          commands:
            - echo "Build step configured for Streamlit container/runtime hosting"
      artifacts:
        baseDirectory: frontend
        files:
          - '**/*'
      cache:
        paths:
          - frontend/.venv/**/*
  EOT

  tags = {
    Name = local.amplify_name
  }
}

resource "aws_amplify_branch" "main" {
  count = var.amplify_enable_branch ? 1 : 0

  app_id            = aws_amplify_app.frontend.id
  branch_name       = var.amplify_branch_name
  stage             = "PRODUCTION"
  framework         = "Web"
  enable_auto_build = true

  environment_variables = {
    API_BASE_URL = aws_apigatewayv2_api.http.api_endpoint
  }

  tags = {
    Name = "${local.amplify_name}-${var.amplify_branch_name}"
  }
}
