variable "aws_region" {
  description = "The AWS region to create things in."
  default = "us-east-2"
}

variable "key_name" {
  description = "The name of the aws key pair to associate with the instance"
}

variable "instance_type" {
  description = "The type of EC2 instance to run"
  default = "m5.xlarge"
}

variable "aws_ami" {
  description = "The Amazon Machine Image to use"
  default = "ami-09aaaa836262a0c46"
}
