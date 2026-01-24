output "repository_url" {
  description = "Repository URL"
  value       = github_repository.voice_clone_settings.html_url
}

output "repository_ssh_url" {
  description = "Repository SSH URL"
  value       = github_repository.voice_clone_settings.ssh_clone_url
}
