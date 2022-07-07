# resource "aws_iam_role" "iam_for_lambda" {
#   name = "iam_for_lambda"
#   assume_role_policy = jsonencode({
#     "Version" : "2012-10-17",
#     "Statement" : [
#       {
#         "Action" : "sts:AssumeRole",
#         "Principal" : {
#           "Service" : "lambda.amazonaws.com"
#         },
#         "Effect" : "Allow",
#         "SID" : ""
#       }
#     ]
#   })
# }

# resource "aws_lambda_permission" "lambda_vpc" {
#     action = "lambda:InvokeFunction"
#     function_name = aws_lambda_function.lambda_vpc.arn
#     principal = "lambda.amazonaws.com"
#     source_arn = aws_vpc.vpc.arn

# }
