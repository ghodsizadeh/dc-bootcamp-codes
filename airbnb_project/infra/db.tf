resource "aws_db_instance" "default" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  db_name              = "mydb"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.tutorial_db_subnet_group.name
  availability_zone    = "eu-west-1b"
  publicly_accessible  = true
  vpc_security_group_ids = [
    aws_security_group.tutorial-db.id,
  ]
}
