#!/bin/bash

# Pre-commit hook to prevent direct commits to protected branches
# This ensures all changes go through feature branches and PRs

set -e

# Get current branch name
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")

# List of protected branches
PROTECTED_BRANCHES=("master" "main" "develop")

# Check if current branch is protected
for protected in "${PROTECTED_BRANCHES[@]}"; do
    if [ "$BRANCH" = "$protected" ]; then
        echo ""
        echo "❌ Error: Cannot commit directly to protected branch '$BRANCH'"
        echo ""
        echo "Protected branches: ${PROTECTED_BRANCHES[*]}"
        echo ""
        echo "💡 To fix this:"
        echo "   1. Create a feature branch:"
        echo "      git checkout -b feature/your-feature-name"
        echo ""
        echo "   2. Make your changes and commit:"
        echo "      git add ."
        echo "      git commit -m \"feat: your feature description\""
        echo ""
        echo "   3. Push your feature branch:"
        echo "      git push origin feature/your-feature-name"
        echo ""
        echo "   4. Create a Pull Request on GitHub"
        echo ""
        echo "📖 See docs/git-workflow.md for more information"
        echo ""
        exit 1
    fi
done

# If we're here, the branch is not protected
exit 0
