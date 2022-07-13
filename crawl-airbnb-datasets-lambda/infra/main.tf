provider "aws" {
  region = "eu-west-1"
}


resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  filename      = "../src.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = "600"
  runtime       = "python3.9"

  memory_size = 3008




  layers = [
    "arn:aws:lambda:eu-west-1:336392948345:layer:AWSDataWrangler-Python39:5"
  ]
  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("../src.zip")


  environment {
    variables = {
      foo = "bar"
    }
  }
}
