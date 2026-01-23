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

# Repository already exists, so we import it instead of creating
# To import: terraform import github_repository.voice_clone voice-clone
data "github_repository" "voice_clone" {
  full_name = "${var.github_owner}/${var.repository_name}"
}

resource "github_branch_default" "master" {
  repository = data.github_repository.voice_clone.name
  branch     = "master"
}

resource "github_branch_protection" "master_protection" {
  repository_id = data.github_repository.voice_clone.node_id
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
  repository_id = data.github_repository.voice_clone.node_id
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
  repository_id = data.github_repository.voice_clone.node_id
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

# Repository files will be managed via git, not Terraform
# resource "github_repository_file" "code_of_conduct" {
#   repository = data.github_repository.voice_clone.name
#   file       = "CODE_OF_CONDUCT.md"
#   content    = file("${path.module}/../CODE_OF_CONDUCT.md")
# }

# resource "github_repository_file" "contributing" {
#   repository = data.github_repository.voice_clone.name
#   file       = "CONTRIBUTING.md"
#   content    = file("${path.module}/../CONTRIBUTING.md")
# }
