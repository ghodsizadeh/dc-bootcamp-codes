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


resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = var.lambda_layers_file
  layer_name          = "airbnb_lambda_layer"
  description         = "airbnb lambda layer"
  compatible_runtimes = ["python3.9"]
  source_code_hash    = filebase64sha256(var.lambda_layers_file)

}

resource "aws_lambda_function" "query_lambda" {

  filename      = var.lambda_query_zip
  function_name = "query_lambda_airbnb"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "query.lambda_handler"
  timeout       = "3"
  runtime       = "python3.9"

  memory_size = 512

  vpc_config {
    security_group_ids = [
      aws_security_group.lambda_sg.id,
    ]
    subnet_ids = [
      aws_subnet.private_subnet_1.id,
      aws_subnet.private_subnet_2.id,
    ]


  }

  layers = [
    aws_lambda_layer_version.lambda_layer.arn,
  ]


  source_code_hash = filebase64sha256(var.lambda_query_zip)


  environment {
    variables = {
      MONGO_PASSWORD = var.docdb_password,
      TEST_URL       = aws_docdb_cluster.docdb.endpoint,
    }
  }
}


### booking
resource "aws_lambda_function" "booking_lambda" {

  filename      = var.lambda_booking_zip
  function_name = "booking_lambda_airbnb"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "booking.lambda_handler"
  timeout       = "3"
  runtime       = "python3.9"

  memory_size = 512

  vpc_config {
    security_group_ids = [
      aws_security_group.lambda_sg.id,
    ]
    subnet_ids = [
      aws_subnet.private_subnet_1.id,
      aws_subnet.private_subnet_2.id,
    ]


  }

  layers = [
    aws_lambda_layer_version.lambda_layer.arn,
  ]


  source_code_hash = filebase64sha256(var.lambda_booking_zip)


  environment {
    variables = {
      MONGO_PASSWORD = var.docdb_password,
      TEST_URL       = aws_docdb_cluster.docdb.endpoint,
    }
  }
}



### Update db
resource "aws_lambda_function" "update_db_lambda" {

  filename      = var.lambda_update_db_zip
  function_name = "update_db_lambda_airbnb"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "update_db.lambda_handler"
  timeout       = "3"
  runtime       = "python3.9"

  memory_size = 512

  vpc_config {
    security_group_ids = [
      aws_security_group.lambda_sg.id,
    ]
    subnet_ids = [
      aws_subnet.private_subnet_1.id,
      aws_subnet.private_subnet_2.id,
    ]


  }

  layers = [
    aws_lambda_layer_version.lambda_layer.arn,
  ]


  source_code_hash = filebase64sha256(var.lambda_update_db_zip)


  environment {
    variables = {
      MONGO_PASSWORD = var.docdb_password,
      TEST_URL       = aws_docdb_cluster.docdb.endpoint,
    }
  }
}

