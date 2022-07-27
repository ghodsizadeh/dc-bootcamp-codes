

resource "aws_docdb_subnet_group" "db_subnet_group" {
  name        = "db_subnet_group"
  description = "db subnet group"
  subnet_ids = [
    aws_subnet.private_subnet_1.id,
    aws_subnet.private_subnet_2.id,
  ]
}
resource "aws_docdb_cluster" "docdb" {
  cluster_identifier      = "main-airbnb-docdb"
  engine                  = "docdb"
  master_username         = var.docdb_username
  master_password         = var.docdb_password
  backup_retention_period = 35
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
  db_subnet_group_name    = aws_docdb_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]




}


resource "aws_docdb_cluster_instance" "cluser_instances" {
  count              = 1
  identifier         = "docdb-cluster-instance-${count.index}"
  cluster_identifier = aws_docdb_cluster.docdb.id
  instance_class     = "db.t3.medium"


}

resource "aws_docdb_cluster_parameter_group" "example" {
  family      = "docdb4.0"
  name        = "docdb-cluster-parameter-group"
  description = "docdb cluster parameter group"

  parameter {
    name  = "tls"
    value = "disabled"
  }
}



