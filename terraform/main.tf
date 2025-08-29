terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" // Match your GitHub secret
}

// --- VPC for Networking ---
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "drowning-detection-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false
}

// --- Managed Database ---
resource "aws_docdb_cluster" "docdb" {
    cluster_identifier      = "drowning-detection-db"
    engine                  = "docdb"
    master_username         = "myuser"
    master_password         = "mypassword" // For production, use a secrets manager
    skip_final_snapshot     = true
}

// We already created ECR repos manually, but for full IaC, you'd define them here too.