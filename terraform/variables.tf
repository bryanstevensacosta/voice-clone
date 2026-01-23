variable "github_token" {
  description = "GitHub personal access token with repo scope"
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "GitHub username or organization"
  type        = string
}

variable "repository_name" {
  description = "Repository name"
  type        = string
  default     = "voice-clone-cli"
}
