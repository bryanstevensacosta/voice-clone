# Git Workflow Guide

This document describes the Git workflow for this project, which enforces a clean, linear history through rebase.

## Table of Contents

- [Overview](#overview)
- [Branch Protection](#branch-protection)
- [Development Workflow](#development-workflow)
- [Pre-Push Hooks](#pre-push-hooks)
- [Commit Message Convention](#commit-message-convention)
- [Common Scenarios](#common-scenarios)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project uses a **rebase-only workflow** to maintain a clean, linear Git history. This means:

- ✅ All changes must be rebased before merging
- ✅ No merge commits allowed
- ✅ Linear history (easy to read and bisect)
- ✅ All changes go through Pull Requests
- ✅ Automated checks enforce the workflow

---

## Branch Protection

### Protected Branches

The following branches have protection rules:
- `master` - Main production branch
- `main` - Alternative main branch (if used)
- `develop` - Development branch (if used)

### Protection Rules

For all protected branches:
- ❌ **No direct pushes** - All changes must go through PRs
- ❌ **No force pushes** - History cannot be rewritten
- ❌ **No deletions** - Branches cannot be deleted
- ✅ **Required status checks** - CI must pass (test, lint, type-check)
- ✅ **Rebase only** - Only rebase merge allowed
- ✅ **Enforce for admins** - Even admins must follow these rules

### Unprotected Branches

All other branches (feature branches, etc.) have no restrictions:
- ✅ Direct pushes allowed
- ✅ Force pushes allowed
- ✅ Can be deleted

---

## Development Workflow

### 1. Start a New Feature

```bash
# Make sure you're on the latest master
git checkout master
git fetch origin
git reset --hard origin/master

# Create a feature branch
git checkout -b feature/my-awesome-feature
```

### 2. Make Changes

```bash
# Make your changes
vim src/voice_clone/cli.py

# Stage and commit
git add src/voice_clone/cli.py
git commit -m "feat: add new CLI command"

# Continue working...
git add tests/test_cli.py
git commit -m "test: add tests for new CLI command"
```

### 3. Keep Your Branch Updated

```bash
# Fetch latest changes
git fetch origin

# Rebase on master (or main/develop)
git rebase origin/master

# If there are conflicts, resolve them:
# 1. Fix conflicts in files
# 2. git add <resolved-files>
# 3. git rebase --continue
```

Or use the Makefile shortcuts:

```bash
make sync              # Fetch and show status
make rebase-master     # Rebase on master
```

### 4. Push Your Branch

```bash
# First push
git push origin feature/my-awesome-feature

# After rebasing (force push required)
git push --force-with-lease origin feature/my-awesome-feature
```

**Note**: The pre-push hook will automatically check if you need to rebase first.

### 5. Create a Pull Request

1. Go to GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill in the PR description
5. Submit the PR

### 6. Wait for CI and Review

- ✅ CI checks must pass (test, lint, type-check)
- ✅ Code review (if applicable)
- ✅ All discussions resolved

### 7. Merge the PR

Once approved, merge via GitHub:
- GitHub will automatically rebase your commits onto the target branch
- Your feature branch will be automatically deleted

---

## Pre-Push Hooks

This project has two pre-push hooks that run automatically:

### 1. Rebase Check Hook

**Purpose**: Ensures your branch is up to date before pushing

**What it checks**:
- ✅ Fetches latest changes from origin
- ✅ Compares your branch with upstream
- ✅ Blocks push if you're behind
- ✅ Prevents direct pushes to protected branches

**Example output**:

```bash
$ git push origin feature/my-feature

🔍 Checking if branch is up to date...
📡 Fetching latest changes from origin...
🔗 Comparing with upstream: origin/feature/my-feature
❌ Error: Your branch is not up to date with origin/feature/my-feature

Your branch is behind the remote. You need to rebase first.

To fix this, run:
  git pull --rebase origin my-feature

Or if you want to rebase on a different branch (e.g., master):
  git fetch origin
  git rebase origin/master
```

### 2. Test Hook

**Purpose**: Runs tests before pushing

**What it checks**:
- ✅ All tests pass
- ✅ Code coverage is above 70%

**Example output**:

```bash
🧪 Running tests...
============================= test session starts ==============================
collected 42 items

tests/test_cli.py ..................                                     [ 42%]
tests/test_audio.py ..................                                   [ 85%]
tests/test_model.py ......                                               [100%]

---------- coverage: platform darwin, python 3.10.16 -----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/voice_clone/__init__.py       2      0   100%
src/voice_clone/cli.py          156     12    92%   45-48, 89-92
src/voice_clone/audio.py         89      5    94%   123-127
src/voice_clone/model.py        134      8    94%   201-208
-----------------------------------------------------------
TOTAL                           381     25    93%

✅ All tests passed!
```

---

## Commit Message Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add voice cloning` |
| `fix` | Bug fix | `fix: resolve audio glitch` |
| `docs` | Documentation | `docs: update README` |
| `style` | Code style | `style: format with black` |
| `refactor` | Code refactoring | `refactor: simplify audio processing` |
| `test` | Tests | `test: add unit tests` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Performance | `perf: optimize model loading` |
| `ci` | CI/CD | `ci: add GitHub Actions` |
| `build` | Build system | `build: update setup.py` |

### Rules

- ✅ Use lowercase for type and description
- ✅ Keep description under 50 characters
- ✅ Use imperative mood ("add" not "added")
- ✅ No period at the end of description
- ✅ Body and footer are optional

### Examples

**Simple commit**:
```bash
git commit -m "feat: add voice synthesis feature"
```

**With scope**:
```bash
git commit -m "fix(audio): resolve sample rate conversion bug"
```

**With body**:
```bash
git commit -m "feat: add batch processing

Allows processing multiple audio files in a single command.
Includes progress bar and error handling."
```

**Breaking change**:
```bash
git commit -m "feat!: change CLI interface

BREAKING CHANGE: The --model flag is now required for all commands."
```

### Validation

The commit-msg hook validates your commit messages automatically:

```bash
$ git commit -m "added new feature"

❌ Error: Commit message does not follow Conventional Commits format

Expected format:
  <type>(<scope>): <description>

Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build

Examples:
  feat: add new feature
  fix(audio): resolve bug
  docs: update README
```

---

## Common Scenarios

### Scenario 1: Your Branch is Behind

**Problem**: You try to push but your branch is behind the remote.

```bash
$ git push origin feature/my-feature
❌ Error: Your branch is not up to date with origin/master
```

**Solution**:

```bash
# Option 1: Rebase on master
git fetch origin
git rebase origin/master
git push --force-with-lease origin feature/my-feature

# Option 2: Use Makefile
make rebase-master
git push --force-with-lease origin feature/my-feature
```

### Scenario 2: Rebase Conflicts

**Problem**: You get conflicts during rebase.

```bash
$ git rebase origin/master
Auto-merging src/voice_clone/cli.py
CONFLICT (content): Merge conflict in src/voice_clone/cli.py
```

**Solution**:

```bash
# 1. Open the conflicted file and resolve conflicts
vim src/voice_clone/cli.py

# 2. Look for conflict markers:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> origin/master

# 3. Edit the file to keep the correct code

# 4. Stage the resolved file
git add src/voice_clone/cli.py

# 5. Continue the rebase
git rebase --continue

# 6. If more conflicts, repeat steps 1-5
# If you want to abort: git rebase --abort
```

### Scenario 3: Accidentally Pushed to Protected Branch

**Problem**: You tried to push directly to master.

```bash
$ git push origin master
❌ Error: Cannot push directly to protected branch 'master'
💡 Create a feature branch and submit a Pull Request instead
```

**Solution**:

```bash
# 1. Create a feature branch from your current position
git checkout -b feature/my-changes

# 2. Push the feature branch
git push origin feature/my-changes

# 3. Create a Pull Request on GitHub

# 4. Reset master to match origin
git checkout master
git reset --hard origin/master
```

### Scenario 4: Need to Update PR After Review

**Problem**: You need to make changes after code review.

**Solution**:

```bash
# 1. Make your changes
vim src/voice_clone/cli.py

# 2. Commit the changes
git add src/voice_clone/cli.py
git commit -m "fix: address review comments"

# 3. Rebase on master to stay up to date
git fetch origin
git rebase origin/master

# 4. Force push to update the PR
git push --force-with-lease origin feature/my-feature

# The PR will automatically update
```

### Scenario 5: Squash Multiple Commits

**Problem**: You have many small commits and want to combine them.

**Solution**:

```bash
# 1. Interactive rebase (last 5 commits)
git rebase -i HEAD~5

# 2. In the editor, change 'pick' to 'squash' (or 's') for commits you want to combine:
# pick abc1234 feat: add feature
# squash def5678 fix: typo
# squash ghi9012 fix: another typo

# 3. Save and close the editor

# 4. Edit the combined commit message

# 5. Force push
git push --force-with-lease origin feature/my-feature
```

### Scenario 6: Check if Rebase is Needed

**Problem**: You want to check if you need to rebase before starting work.

**Solution**:

```bash
# Option 1: Use Makefile
make check-branch

# Option 2: Manual check
git fetch origin
git status -sb

# Option 3: See what's different
git fetch origin
git log HEAD..origin/master --oneline
```

---

## Troubleshooting

### Pre-Push Hook Not Running

**Problem**: The pre-push hook doesn't run when you push.

**Solution**:

```bash
# Reinstall pre-commit hooks
pre-commit install --hook-type pre-push

# Verify installation
ls -la .git/hooks/pre-push
```

### Commit Message Hook Not Running

**Problem**: Invalid commit messages are not being caught.

**Solution**:

```bash
# Reinstall commit-msg hook
pre-commit install --hook-type commit-msg

# Verify installation
ls -la .git/hooks/commit-msg
```

### Force Push Rejected

**Problem**: `git push --force` is rejected.

**Solution**:

Use `--force-with-lease` instead of `--force`:

```bash
# ❌ Don't use this (dangerous)
git push --force origin feature/my-feature

# ✅ Use this (safer)
git push --force-with-lease origin feature/my-feature
```

`--force-with-lease` will fail if someone else pushed to your branch, preventing you from accidentally overwriting their work.

### Rebase Takes Too Long

**Problem**: Rebasing is taking a very long time.

**Solution**:

```bash
# Abort the current rebase
git rebase --abort

# Try rebasing with fewer commits at a time
git rebase -i HEAD~10  # Rebase last 10 commits

# Or rebase in smaller steps
git rebase origin/master~5  # Rebase to 5 commits before master
git rebase origin/master    # Then rebase to master
```

### Lost Commits After Rebase

**Problem**: You lost commits after a rebase.

**Solution**:

```bash
# Find your lost commits in the reflog
git reflog

# Look for your commits (they're not actually lost)
# Example output:
# abc1234 HEAD@{0}: rebase: feat: add feature
# def5678 HEAD@{1}: commit: feat: add feature (this is your lost commit)

# Reset to the commit before the rebase
git reset --hard HEAD@{1}

# Or reset to a specific commit
git reset --hard def5678
```

### Can't Push After Rebase

**Problem**: Push is rejected after rebasing.

```bash
$ git push origin feature/my-feature
! [rejected]        feature/my-feature -> feature/my-feature (non-fast-forward)
```

**Solution**:

This is expected after a rebase. Use force push with lease:

```bash
git push --force-with-lease origin feature/my-feature
```

---

## Quick Reference

### Makefile Commands

```bash
make sync              # Fetch and show status
make rebase-master     # Rebase on master
make rebase-main       # Rebase on main
make rebase-develop    # Rebase on develop
make check-branch      # Check if rebase is needed
make test              # Run tests
make pre-commit        # Run all pre-commit hooks
```

### Git Commands

```bash
# Start new feature
git checkout -b feature/name

# Commit changes
git commit -m "type: description"

# Update branch
git fetch origin
git rebase origin/master

# Push changes
git push origin feature/name
git push --force-with-lease origin feature/name  # After rebase

# Check status
git status -sb
git log --oneline --graph

# Resolve conflicts
git add <file>
git rebase --continue
git rebase --abort  # If you want to cancel
```

### Pre-Commit Commands

```bash
# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

---

## Additional Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Pre-Commit Framework](https://pre-commit.com/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**Remember**: The goal of this workflow is to maintain a clean, linear history that's easy to understand and debug. While it may seem strict at first, it will save time in the long run!
