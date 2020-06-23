output "public_ip" {
  value       = aws_instance.app.public_ip
  description = "The public IP of the web server"
}

output "public_dns" {
  value       = aws_eip.default.public_dns
  description = "The public DNS of the web server"
}