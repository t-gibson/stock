variable "key_name" {
  default = "design_search"
}

variable "instance_type" {
  description = "The type of EC2 instance to run"
  #default     = "p2.xlarge"
  default     = "t2.micro"
}
