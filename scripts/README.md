# Git Hooks Scripts

This directory contains custom Git hooks that enforce the project's workflow and quality standards.

## Overview

All hooks are managed by [pre-commit](https://pre-commit.com/) and configured in `.pre-commit-config.yaml`.

## Available Hooks

### 1. check-branch-before-commit.sh

**Stage**: `pre-commit`
**Purpose**: Prevents direct commits to protected branches

**Protected branches**:
- `master`
- `main`
- `develop`

**What it does**:
- Checks if you're currently on a protected branch
- Blocks the commit if you are
- Provides instructions to create a feature branch

**Example**:
```bash
# This will be blocked
git checkout master
git commit -m "feat: new feature"

# This works
git checkout -b feature/my-feature
git commit -m "feat: new feature"
```

---

### 2. check-merge-to-protected.sh

**Stage**: `pre-merge-commit`
**Purpose**: Prevents merging branches into protected branches locally

**Protected branches**:
- `master`
- `main`
- `develop`

**What it does**:
- Detects when you're trying to merge into a protected branch
- Blocks the merge commit
- Instructs you to use Pull Requests on GitHub instead

**Example**:
```bash
# This will be blocked
git checkout master
git merge feature/my-feature

# Correct workflow
git checkout feature/my-feature
git push origin feature/my-feature
# Then create PR on GitHub
```

---

### 3. check-rebase-before-push.sh

**Stage**: `pre-push`
**Purpose**: Ensures your branch is up to date before pushing

**What it does**:
- Fetches latest changes from origin
- Compares your branch with upstream
- Blocks push if you're behind
- Prevents direct pushes to protected branches

**Example**:
```bash
# If your branch is behind
git push origin feature/my-feature
# Hook will block and tell you to rebase first

# Fix by rebasing
git fetch origin
git rebase origin/master
git push --force-with-lease origin feature/my-feature
```

---

### 4. check-terraform-sync.sh

**Stage**: `manual`
**Purpose**: Checks if Terraform state is in sync with remote

**What it does**:
- Compares local Terraform state with remote
- Warns if there are differences
- Helps prevent state conflicts

**Usage**:
```bash
# Run manually
make check-terraform

# Or directly
./scripts/check-terraform-sync.sh
```

---

## Installation

Hooks are automatically installed when you run:

```bash
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
pre-commit install --hook-type pre-merge-commit
```

Or use the setup script:

```bash
./setup.sh
```

## Testing Hooks

### Test all hooks manually
```bash
pre-commit run --all-files
```

### Test specific hook
```bash
pre-commit run check-branch --all-files
```

### Test pre-push hooks
```bash
pre-commit run --hook-stage push
```

## Bypassing Hooks (Not Recommended)

In rare cases where you need to bypass hooks:

```bash
# Bypass pre-commit hooks
git commit --no-verify -m "message"

# Bypass pre-push hooks
git push --no-verify
```

**⚠️ Warning**: Bypassing hooks should only be done in exceptional circumstances and with good reason. It defeats the purpose of having these protections.

## Troubleshooting

### Hook not running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push --hook-type pre-merge-commit
```

### Hook failing unexpectedly

```bash
# Check hook permissions
ls -la scripts/*.sh

# Make executable if needed
chmod +x scripts/*.sh
```

### Update hooks

```bash
# Update to latest versions
pre-commit autoupdate
```

## Adding New Hooks

1. Create the script in `scripts/` directory
2. Make it executable: `chmod +x scripts/your-script.sh`
3. Add to `.pre-commit-config.yaml` under `local` hooks
4. Install the hook: `pre-commit install --hook-type <type>`
5. Test: `pre-commit run your-hook-id --all-files`

## Hook Development Guidelines

When creating new hooks:

- ✅ Use `#!/bin/bash` shebang
- ✅ Use `set -e` to exit on errors
- ✅ Provide clear, actionable error messages
- ✅ Include emoji for visual clarity (❌, ✅, 💡, 📖)
- ✅ Suggest concrete steps to fix the issue
- ✅ Exit with code 0 for success, non-zero for failure
- ✅ Make scripts idempotent (safe to run multiple times)
- ✅ Test thoroughly before committing

## References

- [Pre-commit documentation](https://pre-commit.com/)
- [Git hooks documentation](https://git-scm.com/docs/githooks)
- [Project Git workflow](../.kiro/steering/git-workflow.md)
