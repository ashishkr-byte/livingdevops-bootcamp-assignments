
terraform {
  required_version = "1.14.1" # this is the terraform cli version

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # this is aWS provider plugin version, i.e. use aws provider version >5
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0" # this is random provider plugin version, i.e. use random provider version >3
    }
  }
}

