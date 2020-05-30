variable "key_name" {
  description = "The name of the aws key pair to associate with the instance"
  default     = "personal"
}

variable "instance_type" {
  description = "The type of EC2 instance to run"
  default     = "t2.micro"
}
