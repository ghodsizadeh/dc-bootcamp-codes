terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.21.0"
    }
  }
}

provider "aws" {
  # Configuration options

  # region = "eu-west-1"
  region = "us-east-1"
}
