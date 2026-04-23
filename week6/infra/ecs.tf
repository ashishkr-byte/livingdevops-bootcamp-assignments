
# ECR repo to store app image

resource "aws_ecr_repository" "app_image" {
  name                 = "${var.prefix}-${var.app_name}"
  image_tag_mutability = "MUTABLE"

  # this could slow down the push and add costs, you want to scan image before the push, but we will learn later how to scan docker images, so below part I will not use

  /* image_scanning_configuration {
    scan_on_push = true 
    
  } */
}
# mutable means you can overwrite tags, can use same tag again 
# immutable means you cannnot use same tag again, and also cannot modify tag, by default its mutable


/* output "ecrrepo" {
  value = aws_ecr_repository.app_image.repository_url
  
}
 */



# ECS components




# ECS cluster

resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.prefix}-${var.app_name}"

  /* setting {
    name  = "containerInsights"
    value = "enabled"
  } */

  # setting ->  Configuration block(s) with cluster settings. For example, this can be used to enable CloudWatch Container Insights for a cluster. but this incurs costs, in prod - OK, but here no need 
}



# Task definition

resource "aws_ecs_task_definition" "taskdefinition" {
  family = var.app_name

  execution_role_arn = "arn:aws:iam::201760452324:role/ecsTaskExecutionRole"
  # this is a required property



  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  network_mode             = "awsvpc"
  # by default the network mode is bridge, but for fargate we have to use awsvpc, and for ec2 launch type we can use both awsvpc and bridge.

  # If the requires_compatibilities is FARGATE,-> then  cpu, memory are also required.

  container_definitions = jsonencode([
    {
      name      = var.app_name
      image     = var.image
      cpu       = 1024
      memory    = 2048
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]

      secrets = [
        {
          name      = "DB_LINK"
          valueFrom = "${aws_secretsmanager_secret.db_secret.arn}:DB_LINK::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-create-group  = "true"
          awslogs-group         = "/ecs/jan26week5-studentportal"
          awslogs-region        = "ap-south-1"
          awslogs-stream-prefix = "ecs"
        }
      }


    }
  ])



}



# secret manager to manage env variables for credentials

resource "aws_secretsmanager_secret" "db_secret" {
  name = "db/${var.app_name}-secrets"

}

resource "aws_secretsmanager_secret_version" "db_secret_value" {
  secret_id = aws_secretsmanager_secret.db_secret.id

  secret_string = jsonencode({

    DB_LINK = "postgresql://${aws_db_instance.default.username}:${random_password.passwordb.result}@${aws_db_instance.default.endpoint}/${aws_db_instance.default.db_name}"

    }
  )
  # DB_LINK = "postgresql://{username}:{password}@{host}:5432/{database_name}"

  # this link contain credentials of db -- so we better fetch value from db_instance resource. look at the attribute references in tf documentation to see what values db_instance returns and then use those values

}

# ECS service

resource "aws_ecs_service" "service" {
  name            = "${var.prefix}-${var.app_name}-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.taskdefinition.arn
  desired_count   = 2
  # iam_role        = aws_iam_role.foo.arn
  # If using awsvpc network mode, do not specify this role, so I have commented it out.

  launch_type = "FARGATE"


  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = [aws_subnet.private1.id, aws_subnet.private2.id]
    security_groups  = [aws_security_group.ecssg.id]
    assign_public_ip = false
  }


  load_balancer {
    target_group_arn = aws_lb_target_group.app_tg.arn
    container_name   = var.app_name
    container_port   = 5000
  }
}


