terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.0"
    }
  }
}

provider "github" {
  token = var.github_token
  owner = var.github_owner
}

resource "github_repository" "voice_clone" {
  name        = var.repository_name
  description = "Personal voice cloning CLI tool using XTTS-v2"
  visibility  = "public"

  has_issues      = true
  has_projects    = false
  has_wiki        = false
  has_downloads   = true

  allow_merge_commit     = false
  allow_squash_merge     = false
  allow_rebase_merge     = true
  delete_branch_on_merge = true

  topics = [
    "voice-cloning",
    "text-to-speech",
    "tts",
    "xtts-v2",
    "coqui",
    "python",
    "cli",
    "machine-learning"
  ]
}

resource "github_branch_default" "master" {
  repository = github_repository.voice_clone.name
  branch     = "master"
}

resource "github_branch_protection" "master_protection" {
  repository_id = github_repository.voice_clone.node_id
  pattern       = "master"

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 0
  }

  required_status_checks {
    strict   = true
    contexts = ["test", "lint", "type-check"]
  }

  enforce_admins         = true
  require_signed_commits = false

  allows_deletions    = false
  allows_force_pushes = false

  required_linear_history = true
}

resource "github_branch_protection" "main_protection" {
  repository_id = github_repository.voice_clone.node_id
  pattern       = "main"

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 0
  }

  required_status_checks {
    strict   = true
    contexts = ["test", "lint", "type-check"]
  }

  enforce_admins         = true
  require_signed_commits = false

  allows_deletions    = false
  allows_force_pushes = false

  required_linear_history = true
}

resource "github_branch_protection" "develop_protection" {
  repository_id = github_repository.voice_clone.node_id
  pattern       = "develop"

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 0
  }

  required_status_checks {
    strict   = true
    contexts = ["test", "lint", "type-check"]
  }

  enforce_admins         = true
  require_signed_commits = false

  allows_deletions    = false
  allows_force_pushes = false

  required_linear_history = true
}

resource "github_repository_file" "code_of_conduct" {
  repository = github_repository.voice_clone.name
  file       = "CODE_OF_CONDUCT.md"
  content    = file("${path.module}/../CODE_OF_CONDUCT.md")
}

resource "github_repository_file" "contributing" {
  repository = github_repository.voice_clone.name
  file       = "CONTRIBUTING.md"
  content    = file("${path.module}/../CONTRIBUTING.md")
}
