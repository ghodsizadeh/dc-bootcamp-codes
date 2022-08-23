resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/20"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

}
resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.16.0/20"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"

}
resource "aws_subnet" "private_subnet_1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.128.0/20"

  availability_zone = "us-east-1a"



}
resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.144.0/20"
  availability_zone = "us-east-1b"




}

resource "aws_security_group" "lambda_sg" {
  vpc_id      = aws_vpc.main.id
  description = "Security group for lambda"
  name        = "lambda_sg"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]


  }
}

resource "aws_security_group" "db_sg" {
  vpc_id      = aws_vpc.main.id
  description = "Security group for db"
  name        = "db_sg"
  # docdb
  ingress {
    description     = "Allow access to docdb"
    from_port       = 27017
    to_port         = 27017
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]

  }
}


