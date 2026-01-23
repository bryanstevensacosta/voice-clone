# Terraform Configuration for GitHub Repository

This directory contains Terraform configuration to set up branch protection rules for the GitHub repository.

## Quick Start

```bash
cd terraform

# 1. Copy the example configuration
cp terraform.tfvars.example terraform.tfvars

# 2. Edit with your GitHub token and username
vim terraform.tfvars

# 3. Run the setup script
./setup-branch-protection.sh
```

That's it! The script will initialize Terraform, show you the planned changes, and apply them.

## Prerequisites

1. Install Terraform:
   ```bash
   brew install terraform
   ```

2. Create a GitHub Personal Access Token:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Copy the token (you won't see it again)

## Manual Usage (Alternative)

### 1. Create Configuration File

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your values:
```hcl
github_token    = "ghp_your_token_here"
github_owner    = "bryanstevensacosta"
repository_name = "voice-clone"
```

### 2. Initialize Terraform

```bash
cd terraform
terraform init
```

This will download the GitHub provider plugin.

### 3. Plan Changes

Preview what Terraform will create:

```bash
terraform plan
```

### 4. Apply Configuration

Create the branch protection rules:

```bash
terraform apply
```

Type `yes` when prompted to confirm.

### 5. Verify

After applying, Terraform will output:
- `repository_url`: The HTTPS URL of your repository
- `repository_ssh_url`: The SSH URL of your repository

Visit your repository on GitHub and check:
- Settings → Branches → Branch protection rules
- Verify that `master`, `main`, and `develop` branches have protection enabled

## Configuration Details

### Branch Protection Rules

The configuration sets up the following protection for the `master`, `main`, and `develop` branches:

- **Required pull request reviews**: 0 approvals required (solo maintainer)
- **Required status checks**: Must pass before merging
  - `test`: Test suite must pass
  - `lint`: Linting must pass
  - `type-check`: Type checking must pass
- **Linear history**: Enforced (no merge commits)
- **Force pushes**: Disabled
- **Branch deletions**: Disabled
- **Enforce admins**: Enabled (even admins must follow these rules)

### Repository Settings

- **Visibility**: Public
- **Merge strategies**: Only rebase merge allowed
- **Auto-delete branches**: Enabled after merge
- **Topics**: voice-cloning, text-to-speech, tts, xtts-v2, coqui, python, cli, machine-learning

## Using Environment Variables (Alternative)

Instead of using `terraform.tfvars`, you can use environment variables:

```bash
export TF_VAR_github_token="YOUR_GITHUB_TOKEN"
export TF_VAR_github_owner="bryanstevensacosta"
export TF_VAR_repository_name="voice-clone"

terraform plan
terraform apply
```

## Important Notes

1. **Security**: Never commit your GitHub token to version control
2. **State file**: The `terraform.tfstate` file contains sensitive information. It's already in `.gitignore`
3. **Repository**: This configuration uses the existing `voice-clone` repository

## Cleanup

To destroy all branch protection rules created by Terraform:

```bash
terraform destroy
```

**Warning**: This will remove all branch protection rules!

## Troubleshooting

### Error: Branch protection requires status checks that don't exist

The status checks (`test`, `lint`, `type-check`) must exist before branch protection can require them.

**Solution**: You have two options:

1. **Push code first, then apply Terraform** (Recommended):
   ```bash
   # Push your code to trigger CI
   git push origin feat/initial-setup

   # Wait for CI to run once
   # Then apply Terraform
   cd terraform
   ./setup-branch-protection.sh
   ```

2. **Temporarily disable status checks**:
   - Comment out the `required_status_checks` block in `main.tf`
   - Apply Terraform
   - After CI runs once, uncomment and apply again

### Error: Authentication failed

Make sure your GitHub token has the `repo` scope and is still valid.
