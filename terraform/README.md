# Terraform Configuration for GitHub Repository

This directory contains Terraform configuration to set up the GitHub repository with branch protection rules.

## Prerequisites

1. Install Terraform:
   ```bash
   brew install terraform
   ```

2. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Copy the token (you won't see it again)

## Usage

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

This will download the GitHub provider plugin.

### 2. Plan Changes

Preview what Terraform will create:

```bash
terraform plan \
  -var="github_token=YOUR_GITHUB_TOKEN" \
  -var="github_owner=YOUR_GITHUB_USERNAME"
```

Replace:
- `YOUR_GITHUB_TOKEN` with your GitHub personal access token
- `YOUR_GITHUB_USERNAME` with your GitHub username

### 3. Apply Configuration

Create the repository and branch protection rules:

```bash
terraform apply \
  -var="github_token=YOUR_GITHUB_TOKEN" \
  -var="github_owner=YOUR_GITHUB_USERNAME"
```

Type `yes` when prompted to confirm.

### 4. Verify

After applying, Terraform will output:
- `repository_url`: The HTTPS URL of your repository
- `repository_ssh_url`: The SSH URL of your repository

Visit your repository on GitHub and check:
- Settings → Branches → Branch protection rules
- Verify that `master` branch has protection enabled

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

## Using Environment Variables (Recommended)

Instead of passing variables on the command line, you can use environment variables:

```bash
export TF_VAR_github_token="YOUR_GITHUB_TOKEN"
export TF_VAR_github_owner="YOUR_GITHUB_USERNAME"

terraform plan
terraform apply
```

Or create a `terraform.tfvars` file (DO NOT commit this file):

```hcl
github_token = "YOUR_GITHUB_TOKEN"
github_owner = "YOUR_GITHUB_USERNAME"
repository_name = "voice-clone-cli"
```

Then run:
```bash
terraform plan
terraform apply
```

## Important Notes

1. **Security**: Never commit your GitHub token to version control
2. **State file**: The `terraform.tfstate` file contains sensitive information. Add it to `.gitignore`
3. **Existing repository**: If the repository already exists, you may need to import it first:
   ```bash
   terraform import github_repository.voice_clone voice-clone-cli
   ```

## Cleanup

To destroy all resources created by Terraform:

```bash
terraform destroy \
  -var="github_token=YOUR_GITHUB_TOKEN" \
  -var="github_owner=YOUR_GITHUB_USERNAME"
```

**Warning**: This will delete the repository and all its contents!

## Troubleshooting

### Error: Repository already exists

If you get an error that the repository already exists, you have two options:

1. Import the existing repository:
   ```bash
   terraform import github_repository.voice_clone voice-clone-cli
   ```

2. Or remove the `github_repository` resource from `main.tf` and only manage branch protection

### Error: Branch protection requires status checks that don't exist

The status checks (`test`, `lint`, `type-check`) must exist before branch protection can require them. You may need to:

1. Push code and trigger the CI workflow first
2. Or temporarily comment out the `required_status_checks` block in `main.tf`
3. Apply Terraform
4. After CI runs once, uncomment and apply again
