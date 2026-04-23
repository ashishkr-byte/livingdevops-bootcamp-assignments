
provider "aws" {
  region = "ap-south-1"

  default_tags {
    tags = {
      repo      = "jan26"
      terraform = true
    }
  }
}



terraform {
  backend "s3" {
    bucket  = "state-bucket-jan26"
    key     = "jan26/week6/terraform.tfstate"
    region  = "ap-south-1"
    encrypt = true
    # means this will use default AWS KMS key, if you want use own key, you define it as below:
    # kms_key_id = "value"
  }
}