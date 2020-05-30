provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_s3_bucket" "app_files" {
  bucket = "search-indices-data-store"
}

resource "aws_instance" "app" {
  ami           = "ami-2757f631"
  instance_type = var.instance_type
  key_name      = var.key_name
}
