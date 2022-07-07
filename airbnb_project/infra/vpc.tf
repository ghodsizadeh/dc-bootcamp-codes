data "aws_vpc" "main" {
  state = "available"
}

resource "aws_security_group" "tutorial" {
  name        = "tutorial-securitygroup"
  description = "Tutorial Security Group"
  vpc_id      = data.aws_vpc.main.id

  tags = {
    Name = "tutorial-securitygroup"
  }
}


resource "aws_security_group" "tutorial-db" {
  name        = "tutorial-db-securitygroup"
  description = "Tutorial DB Security Group"
  vpc_id      = data.aws_vpc.main.id
  tags = {
    Name = "tutorial-db-securitygroup"
  }

}
resource "aws_security_group_rule" "ssh" {
  type              = "ingress"
  protocol          = "TCP"
  from_port         = 22
  to_port           = 22
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.tutorial.id

}

resource "aws_security_group_rule" "http" {
  type              = "ingress"
  protocol          = "TCP"
  from_port         = 80
  to_port           = 80
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.tutorial.id

}
resource "aws_security_group_rule" "rds-mysql" {
  type      = "ingress"
  protocol  = "TCP"
  from_port = 3306
  to_port   = 3306
  # cidr_blocks       = ["0.0.0.0/0"]
  security_group_id        = aws_security_group.tutorial-db.id
  source_security_group_id = aws_security_group.tutorial.id

}
resource "aws_security_group_rule" "rds-mysqlout" {
  type      = "egress"
  protocol  = "TCP"
  from_port = 3306
  to_port   = 3306
  # cidr_blocks       = ["0.0.0.0/0"]
  security_group_id        = aws_security_group.tutorial-db.id
  source_security_group_id = aws_security_group.tutorial.id
}


data "aws_subnet" "db_subnet_1" {
  availability_zone_id = "euw1-az2"
}
data "aws_subnet" "db_subnet_2" {
  availability_zone_id = "euw1-az1"
}


resource "aws_db_subnet_group" "tutorial_db_subnet_group" {
  name        = "tutorial-db-subnet-group"
  description = "Tutorial DB Subnet Group"
  subnet_ids  = [data.aws_subnet.db_subnet_1.id, data.aws_subnet.db_subnet_2.id]


}
