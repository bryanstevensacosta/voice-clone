#!/bin/bash
set -e

echo "🔧 Setting up GitHub Branch Protection with Terraform"
echo ""

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed"
    echo "Install it with: brew install terraform"
    exit 1
fi

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found"
    echo ""
    echo "Please create terraform.tfvars from the example:"
    echo "  cp terraform.tfvars.example terraform.tfvars"
    echo ""
    echo "Then edit it with your GitHub token and username:"
    echo "  vim terraform.tfvars"
    echo ""
    echo "To create a GitHub token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Select scope: 'repo' (full control)"
    echo "  4. Copy the token and paste it in terraform.tfvars"
    exit 1
fi

echo "✓ terraform.tfvars found"
echo ""

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init
echo ""

# Plan
echo "📋 Planning changes..."
terraform plan
echo ""

# Ask for confirmation
read -p "Do you want to apply these changes? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Aborted"
    exit 0
fi

# Apply
echo ""
echo "🚀 Applying changes..."
terraform apply -auto-approve
echo ""

echo "✅ Branch protection rules configured!"
echo ""
echo "You can now push your code to GitHub."
echo "The following branches are protected:"
echo "  - master"
echo "  - main"
echo "  - develop"
echo ""
echo "Protection rules:"
echo "  ✓ Require pull requests"
echo "  ✓ Require status checks (test, lint, type-check)"
echo "  ✓ Require linear history (rebase only)"
echo "  ✓ No force pushes"
echo "  ✓ No deletions"
echo "  ✓ Enforce for admins"
