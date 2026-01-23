#!/bin/bash
# Pre-push hook to ensure branch is rebased before pushing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 Checking if branch is up to date...${NC}"

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Skip check for master, main, develop (protected branches shouldn't be pushed directly anyway)
if [[ "$CURRENT_BRANCH" == "master" ]] || [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "develop" ]]; then
    echo -e "${RED}❌ Error: Cannot push directly to protected branch '$CURRENT_BRANCH'${NC}"
    echo -e "${YELLOW}💡 Create a feature branch and submit a Pull Request instead${NC}"
    exit 1
fi

# Fetch latest from origin
echo "📡 Fetching latest changes from origin..."
git fetch origin --quiet

# Determine upstream branch
UPSTREAM_BRANCH=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "")

# If no upstream is set, try to guess it
if [ -z "$UPSTREAM_BRANCH" ]; then
    # Check if branch exists on origin
    if git ls-remote --heads origin "$CURRENT_BRANCH" | grep -q "$CURRENT_BRANCH"; then
        UPSTREAM_BRANCH="origin/$CURRENT_BRANCH"
    else
        # No upstream, this is a new branch - allow push
        echo -e "${GREEN}✅ New branch detected, no rebase needed${NC}"
        exit 0
    fi
fi

echo "🔗 Comparing with upstream: $UPSTREAM_BRANCH"

# Check if upstream branch exists
if ! git rev-parse --verify "$UPSTREAM_BRANCH" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ New branch detected, no rebase needed${NC}"
    exit 0
fi

# Get the merge base
MERGE_BASE=$(git merge-base HEAD "$UPSTREAM_BRANCH" 2>/dev/null || echo "")

if [ -z "$MERGE_BASE" ]; then
    echo -e "${YELLOW}⚠️  Warning: Cannot determine merge base, allowing push${NC}"
    exit 0
fi

# Get the upstream commit
UPSTREAM_COMMIT=$(git rev-parse "$UPSTREAM_BRANCH")

# Check if we're up to date
if [ "$MERGE_BASE" != "$UPSTREAM_COMMIT" ]; then
    echo -e "${RED}❌ Error: Your branch is not up to date with $UPSTREAM_BRANCH${NC}"
    echo ""
    echo -e "${YELLOW}Your branch is behind the remote. You need to rebase first.${NC}"
    echo ""
    echo "To fix this, run:"
    echo -e "${GREEN}  git fetch origin${NC}"
    echo -e "${GREEN}  git rebase origin/$(echo $CURRENT_BRANCH | sed 's/.*\///')${NC}"
    echo ""
    echo "Or if you want to rebase on a different branch (e.g., master):"
    echo -e "${GREEN}  git fetch origin${NC}"
    echo -e "${GREEN}  git rebase origin/master${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Branch is up to date, proceeding with push${NC}"
exit 0
