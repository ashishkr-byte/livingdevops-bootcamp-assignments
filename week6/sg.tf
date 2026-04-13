
# security grp for alb sg


resource "aws_security_group" "albsg" {
  name        = "${var.prefix}-${var.app_name}-albsg"
  description = "for alb"
  vpc_id      = aws_vpc.main.id

  ingress = [
    {
      description = "Allow HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids   = []
      security_groups   = []
      self              = false
    },
    {
      description = "Allow HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids   = []
      security_groups   = []
      self              = false
    }
  ]

  # Inline egress rules (multiple in one block)
  egress = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
      prefix_list_ids   = []
      security_groups   = []
      self              = false
    }
  ]


  tags = {
    Name = "${var.app_name}-albsg"
  }
}



# ECS SG

resource "aws_security_group" "ecssg" {
  name        = "${var.prefix}-${var.app_name}-ecssg"
  description = "for ecs tasks"
  vpc_id      = aws_vpc.main.id

  ingress = [
    {
      description = "Allow traffic from ALB"
      from_port   = var.container_port
      to_port     = var.container_port
      protocol    = "tcp"
      security_groups = [aws_security_group.albsg.id]
      cidr_blocks = []
      ipv6_cidr_blocks = []
      prefix_list_ids   = []
      self              = false
    }
  ]

  egress = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
      prefix_list_ids   = []
      security_groups   = []
      self              = false
    }
  ]

  tags = {
    Name = "${var.app_name}-ecssg"
  }
}


# rds sg

resource "aws_security_group" "rdssg" {
  name        = "${var.prefix}-${var.app_name}-rdssg"
  description = "for rds instance"
  vpc_id      = aws_vpc.main.id

  ingress = [
    {
      cidr_blocks = []
      description = "Allow traffic from ECS tasks"
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      security_groups = [aws_security_group.ecssg.id]
      ipv6_cidr_blocks = []
      prefix_list_ids   = []
      self              = false
    }
  ]

  egress = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
      prefix_list_ids   = []
      security_groups   = []
      self              = false
    }
  ]
}