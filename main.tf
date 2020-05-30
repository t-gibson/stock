provider "aws" {
  region = var.aws_region
}

resource "aws_eip" "default" {
  instance = aws_instance.app.id
  vpc      = true
}

resource "aws_security_group" "default" {
  name        = "default_sg"
  description = "Default security group to access the instances over SSH and HTTP"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "app_files" {
  bucket = "search-indices-data-store"
}

resource "aws_instance" "app" {
  instance_type   = var.instance_type
  ami             = "ami-2757f631"
  key_name        = var.key_name
  security_groups = [aws_security_group.default.name]
  // later we can add here a user data step to install requirements
  // user_data = file("userdata.sh")

  tags = {
    Name = "design-search-app"
  }
}
