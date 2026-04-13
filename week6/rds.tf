
# DB subnet group

resource "aws_db_subnet_group" "default" {
  name       = "${var.prefix}-${var.app_name}-db-subnet-group"
  subnet_ids = [aws_subnet.rds_subnet1.id, aws_subnet.rds_subnet2.id]

}

# password for the database (A-Za-z0-9) --> store in secrets manager

# we will generate a random password, for this we have random plugin just like we have aws plugin, so in the versions.tf file we have a random block like we wrote an aws block

resource "random_password" "passwordb" {
  length           = 10
  special          = false
  override_special = "abcdefghilsjds"
}



# creation of rds instance


resource "aws_db_instance" "default" {
  identifier           = "${var.prefix}-${var.app_name}-db"
  allocated_storage    = 20
  db_name              = "studentportal"
  engine               = "postgres"
  engine_version       = "16.12"
  instance_class       = "db.t3.micro"
  username             = "postgres"
  password             = random_password.passwordb.result
  db_subnet_group_name = aws_db_subnet_group.default.name
  parameter_group_name = "default.postgres16"
  skip_final_snapshot  = true
  publicly_accessible  = false
  vpc_security_group_ids = [ aws_security_group.rdssg.id ]
}




# secret manager create


# create secrets in secret manager (version)
