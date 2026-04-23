
variable "aws_region" {
  type        = string
  description = "aws region"
  default     = "ap-south-1"
}

variable "vpc_name" {
  type        = string
  description = "value"
  default     = "jan26week5"

}

# there is also option to provide the value of variable like region at runtime. If not provided, the default is used.



variable "primary_az" {
  type        = string
  description = "primary Avialability Zone"
  default     = "ap-south-1a"
}



variable "secondary_az" {
  type        = string
  description = "secondary Avialability Zone"
  default     = "ap-south-1b"
}


variable "app_name" {
  type        = string
  description = ""
  default     = "student-portal"
}


variable "prefix" {
  default = "jan26-bootcamp"
}


variable "image" {
  type    = string
  default = "201760452324.dkr.ecr.ap-south-1.amazonaws.com/jan26-bootcamp-student-portal:1.0"
  # the arn of the ecr repo which has image.

  # <act_id>.dkr.ecr.<aws_region>.amazonaws.com/<repo_name>[:tag]

}


variable "container_port" {
  type    = number
  default = 5000

}


/* variable "db_link" {
  type = string
  default = ""
} */


variable "domain_name" {
  type    = string
  default = "ashishkrtech.xyz"
}


variable "alb_zone_id" {
  type    = string
  default = "ZP97RAFLXTNZK"
}