
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
                 "Action": "sts:AssumeRole"

        }
    ]
}
EOF
}

resource "aws_iam_policy" "full_access_s3_buckets" {
  name = "full_access_s3_buckets_policy_1"

  policy = <<EOF
{
 	"Version": "2012-10-17",
 	"Statement": [{
 		"Sid": "ExamplePolicy",
 		"Action": [
 			"s3:*"
 		],
 		"Effect": "Allow",
 		"Resource": [
 			"arn:aws:s3:::my-airbnb-csv/*"
 		]
 	}]
 }
EOF
}

resource "aws_iam_policy_attachment" "full_s3_attach" {
  name       = "full_access_s3_buckets_policy_attachment"
  policy_arn = aws_iam_policy.full_access_s3_buckets.arn
  roles = [
    aws_iam_role.iam_for_lambda.name
  ]

}



