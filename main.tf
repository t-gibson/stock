provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "tls_private_key" "deployer_keys" {
  algorithm   = "RSA"
  ecdsa_curve = "P384"
}

resource "aws_key_pair" "generated_key" {
  key_name   = var.key_name
  public_key = tls_private_key.deployer_keys.public_key_openssh
}

resource "aws_s3_bucket" "app_files" {
  bucket = "search-indices-data-store"
}

resource "aws_instance" "app" {
  ami           = "ami-2757f631"
  instance_type = var.instance_type
  key_name      = aws_key_pair.generated_key.key_name
}
