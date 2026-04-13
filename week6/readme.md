# ECS- 2 tier app in terraform

- VPC
    - 2 priv subnets
    - 2 public subnets
    - 2 rds subnets (private)
    
    - 2 Route Tables
    - associate private/public subnets to respective RTs
    - one NAT gw
    - routes for public and private part

    - 3 SG for rds, ecs and alb
    - open the port wherever needed
    
- ALB
    - target group
    - ALB (pub subnet)
    - listener for port 80
    - ACM cert for ssl 
    - Listen for https - 443

    - Imp - configuring WAF WAF is an AWS appln level firewall -- if anyone tires DDOS attack, WAF has system and rules which can avoid that attack 

- APP
    - ecr repo
    - push app image (manual way)
    - ECS task definition
    - ECS Clusters
    - ECS services
    - App autoscaling (manual and Terraform)

- DNS
    - route 53 public zones
    - create route to ALB
    - ACM certificate validation

-DB
    - rds 
    - secret manager for password
    - generate a random password
    - encrypting my database with KMS key



    

