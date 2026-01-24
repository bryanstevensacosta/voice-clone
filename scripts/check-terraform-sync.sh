#!/bin/bash

# Check if Terraform state is in sync with remote
# This script ensures local Terraform state matches what's deployed

set -e

TERRAFORM_DIR="terraform"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Checking Terraform state synchronization..."

# Check if terraform directory exists
if [ ! -d "$TERRAFORM_DIR" ]; then
    echo -e "${YELLOW}⚠️  No terraform directory found. Skipping check.${NC}"
    exit 0
fi

cd "$TERRAFORM_DIR"

# Check if terraform is initialized
if [ ! -d ".terraform" ]; then
    echo -e "${YELLOW}⚠️  Terraform not initialized. Run 'terraform init' first.${NC}"
    exit 0
fi

# Check if there are any uncommitted changes in terraform files
if git diff --quiet HEAD -- *.tf *.tfvars 2>/dev/null; then
    echo -e "${GREEN}✓ No uncommitted Terraform changes${NC}"
else
    echo -e "${YELLOW}⚠️  You have uncommitted changes in Terraform files${NC}"
    echo "   Please commit or stash them before proceeding."
    git diff --name-only HEAD -- *.tf *.tfvars 2>/dev/null | sed 's/^/   - /'
    exit 1
fi

# Run terraform plan to check for drift
echo "📋 Running terraform plan to check for drift..."
if terraform plan -detailed-exitcode -out=/dev/null > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Terraform state is in sync with remote${NC}"
    exit 0
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 2 ]; then
        echo -e "${RED}❌ Terraform state has drifted from remote!${NC}"
        echo ""
        echo "Your local Terraform state doesn't match what's deployed."
        echo "This could mean:"
        echo "  1. Someone made changes directly in GitHub"
        echo "  2. You need to pull latest changes"
        echo "  3. You have local changes that need to be applied"
        echo ""
        echo "To fix this:"
        echo "  1. Review the changes: cd terraform && terraform plan"
        echo "  2. If changes are expected: terraform apply"
        echo "  3. If changes are unexpected: investigate and sync"
        echo ""
        exit 1
    else
        echo -e "${RED}❌ Terraform plan failed${NC}"
        echo "Run 'cd terraform && terraform plan' to see the error"
        exit 1
    fi
fi
