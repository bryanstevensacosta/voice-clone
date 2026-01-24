#!/bin/bash

# Pre-merge-commit hook to prevent merging into protected branches
# This ensures all merges to protected branches happen through PRs on GitHub

set -e

# Get current branch name (the branch being merged INTO)
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")

# List of protected branches
PROTECTED_BRANCHES=("master" "main" "develop")

# Check if we're in a merge
if [ -f .git/MERGE_HEAD ]; then
    # Get the branch being merged FROM
    MERGE_BRANCH=$(git reflog -1 | grep -oP "merge \K[^:]+")

    # Check if current branch (merge target) is protected
    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [ "$CURRENT_BRANCH" = "$protected" ]; then
            echo ""
            echo "❌ Error: Cannot merge into protected branch '$CURRENT_BRANCH'"
            echo ""
            echo "Protected branches: ${PROTECTED_BRANCHES[*]}"
            echo ""
            echo "💡 Merges to protected branches must happen through Pull Requests on GitHub"
            echo ""
            echo "To fix this:"
            echo "   1. Abort the current merge:"
            echo "      git merge --abort"
            echo ""
            echo "   2. Push your feature branch:"
            echo "      git checkout $MERGE_BRANCH"
            echo "      git push origin $MERGE_BRANCH"
            echo ""
            echo "   3. Create a Pull Request on GitHub:"
            echo "      - Go to your repository on GitHub"
            echo "      - Click 'New Pull Request'"
            echo "      - Select your feature branch"
            echo "      - Submit the PR for review"
            echo ""
            echo "   4. After approval, merge via GitHub (not locally)"
            echo ""
            echo "📖 See docs/git-workflow.md for more information"
            echo ""
            exit 1
        fi
    done
fi

# If we're here, either not in a merge or target is not protected
exit 0
