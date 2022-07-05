data "aws_vpc" "main" {
  state = "available"
}

resource "aws_security_group" "tutorial" {
  name        = "tutorial-securitygroup"
  description = "Tutorial Security Group"
  vpc_id      = data.aws_vpc.main.id

  # inbound rules for ssh and http from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "ssh"
    cidr_blocks = []
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = []
  }
  tags = {
    Name = "tutorial-securitygroup"
  }
}


resource "aws_security_group" "tutorial-db" {
  name        = "tutorial-db-securitygroup"
  description = "Tutorial DB Security Group"
  vpc_id      = data.aws_vpc.main.id

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"

  }

}
