#########
# Query lambda function
#########

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda_airbnb"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Effect" : "Allow",
        "Sid" : ""
      }
    ]
  })

}


resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole" {
  role       = aws_iam_role.iam_for_lambda.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}



resource "aws_lambda_function" "query_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  filename      = var.lambda_query_zip
  function_name = "query_lambda_airbnb"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "query.lambda_handler"
  timeout       = "30"
  runtime       = "python3.9"

  memory_size = 512

  vpc_config {
    security_group_ids = [
      data.aws_security_group.default.id
    ]
    subnet_ids = [
      data.aws_subnet.subnet_1.id,
      data.aws_subnet.subnet_2.id,
      data.aws_subnet.subnet_3.id,
    ]

  }




  layers = [
    "arn:aws:lambda:eu-west-1:336392948345:layer:AWSDataWrangler-Python39:5"
  ]
  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256(var.lambda_query_zip)


  environment {
    variables = {
      MONGO_PASSWORD = var.docdb_password,
      TEST_URL       = aws_docdb_cluster.docdb.endpoint,
    }
  }
}
