output "repository_url" {
  description = "Repository URL"
  value       = data.github_repository.voice_clone.html_url
}

output "repository_ssh_url" {
  description = "Repository SSH URL"
  value       = data.github_repository.voice_clone.ssh_clone_url
}
