resource "aws_dynamodb_table" "focus_plans" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "planId"

  attribute {
    name = "planId"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = var.dynamodb_table_name
  }
}
