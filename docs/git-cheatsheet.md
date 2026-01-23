# Git Cheatsheet - Quick Reference

Quick reference for common Git operations in this project.

## Daily Workflow

### Starting Work

```bash
# Update master to latest
git checkout master
git fetch origin
git reset --hard origin/master

# Create feature branch
git checkout -b feature/my-feature
```

### Making Changes

```bash
# Stage changes
git add <file>              # Stage specific file
git add .                   # Stage all changes

# Commit with conventional commit message
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"

# Amend last commit (if needed)
git commit --amend
```

### Keeping Branch Updated

```bash
# Fetch latest changes
git fetch origin

# Rebase on master
git rebase origin/master

# If conflicts occur:
# 1. Fix conflicts in files
# 2. git add <resolved-files>
# 3. git rebase --continue
# Or abort: git rebase --abort
```

### Pushing Changes

```bash
# First push
git push origin feature/my-feature

# After rebase (force push)
git push --force-with-lease origin feature/my-feature
```

## Makefile Shortcuts

```bash
make sync              # Fetch and show status
make rebase-master     # Rebase on origin/master
make rebase-main       # Rebase on origin/main
make rebase-develop    # Rebase on origin/develop
make check-branch      # Check if rebase needed
make test              # Run tests
make pre-commit        # Run all pre-commit hooks
```

## Branch Management

### Creating Branches

```bash
# From current branch
git checkout -b feature/new-feature

# From specific branch
git checkout -b feature/new-feature master

# From specific commit
git checkout -b feature/new-feature abc1234
```

### Switching Branches

```bash
# Switch to existing branch
git checkout feature/my-feature

# Switch to master and update
git checkout master
git fetch origin
git reset --hard origin/master
```

### Deleting Branches

```bash
# Delete local branch
git branch -d feature/old-feature

# Force delete local branch
git branch -D feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

## Viewing History

```bash
# View commit history
git log
git log --oneline
git log --oneline --graph
git log --oneline --graph --all

# View changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff master            # Compare with master

# View file history
git log -- <file>
git log -p -- <file>       # With diffs

# View who changed what
git blame <file>
```

## Undoing Changes

### Unstage Changes

```bash
# Unstage specific file
git reset HEAD <file>

# Unstage all files
git reset HEAD
```

### Discard Changes

```bash
# Discard changes in specific file
git checkout -- <file>

# Discard all changes
git checkout -- .

# Clean untracked files (careful!)
git clean -fd
```

### Undo Commits

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo multiple commits
git reset --hard HEAD~3

# Undo to specific commit
git reset --hard abc1234
```

### Revert Commits

```bash
# Create new commit that undoes a commit
git revert abc1234

# Revert multiple commits
git revert abc1234..def5678
```

## Rebasing

### Basic Rebase

```bash
# Rebase on master
git fetch origin
git rebase origin/master

# Rebase on specific branch
git rebase origin/develop

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort
```

### Interactive Rebase

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Rebase from specific commit
git rebase -i abc1234

# Commands in interactive rebase:
# pick   = use commit
# reword = use commit, but edit message
# edit   = use commit, but stop for amending
# squash = use commit, but meld into previous
# fixup  = like squash, but discard message
# drop   = remove commit
```

### Squashing Commits

```bash
# Squash last 3 commits
git rebase -i HEAD~3

# In editor, change 'pick' to 'squash' for commits to combine
# Save and edit the combined commit message
```

## Stashing

```bash
# Stash current changes
git stash
git stash save "work in progress"

# List stashes
git stash list

# Apply stash
git stash apply              # Keep stash
git stash pop               # Apply and remove stash

# Apply specific stash
git stash apply stash@{2}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

## Checking Status

```bash
# Basic status
git status

# Short status
git status -s
git status -sb              # With branch info

# Show what would be committed
git diff --cached

# Show all changes
git diff HEAD
```

## Remote Operations

### Viewing Remotes

```bash
# List remotes
git remote -v

# Show remote details
git remote show origin
```

### Fetching

```bash
# Fetch all remotes
git fetch --all

# Fetch specific remote
git fetch origin

# Fetch and prune deleted branches
git fetch --prune
```

### Pushing

```bash
# Push to remote
git push origin feature/my-feature

# Force push (safer)
git push --force-with-lease origin feature/my-feature

# Push and set upstream
git push -u origin feature/my-feature

# Push all branches
git push --all origin

# Push tags
git push --tags
```

## Commit Message Convention

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance
- `perf`: Performance
- `ci`: CI/CD
- `build`: Build system

### Examples

```bash
git commit -m "feat: add voice cloning"
git commit -m "fix: resolve audio bug"
git commit -m "docs: update README"
git commit -m "test: add unit tests"
git commit -m "chore: update dependencies"
```

## Troubleshooting

### Find Lost Commits

```bash
# View reflog
git reflog

# Recover lost commit
git reset --hard HEAD@{1}
git cherry-pick abc1234
```

### Fix Wrong Branch

```bash
# Move commits to new branch
git branch feature/correct-branch
git reset --hard origin/master
git checkout feature/correct-branch
```

### Undo Force Push

```bash
# Find commit before force push
git reflog

# Reset to that commit
git reset --hard HEAD@{1}

# Force push again (if needed)
git push --force-with-lease origin feature/my-feature
```

### Clean Up Local Branches

```bash
# List merged branches
git branch --merged

# Delete merged branches
git branch --merged | grep -v "\*" | grep -v "master" | xargs -n 1 git branch -d

# Prune remote tracking branches
git fetch --prune
```

## Pre-Commit Hooks

### Install Hooks

```bash
# Install all hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

### Run Hooks

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run ruff --all-files

# Update hooks
pre-commit autoupdate
```

## Useful Aliases

Add these to your `~/.gitconfig`:

```ini
[alias]
    # Short status
    st = status -sb

    # Pretty log
    lg = log --oneline --graph --decorate
    lga = log --oneline --graph --decorate --all

    # Amend last commit
    amend = commit --amend --no-edit

    # Undo last commit (keep changes)
    undo = reset --soft HEAD~1

    # Update master
    um = !git checkout master && git fetch origin && git reset --hard origin/master

    # Rebase on master
    rom = !git fetch origin && git rebase origin/master

    # Force push with lease
    fpush = push --force-with-lease

    # Show branches
    br = branch -vv

    # Show remotes
    rem = remote -v
```

Usage:
```bash
git st                  # git status -sb
git lg                  # git log --oneline --graph
git um                  # Update master
git rom                 # Rebase on master
git fpush origin branch # Force push with lease
```

## Emergency Commands

### Completely Reset to Remote

```bash
# WARNING: This will discard ALL local changes
git fetch origin
git reset --hard origin/master
git clean -fd
```

### Recover Deleted Branch

```bash
# Find the commit
git reflog

# Recreate branch
git checkout -b recovered-branch abc1234
```

### Fix Detached HEAD

```bash
# Create branch from current position
git checkout -b temp-branch

# Or go back to master
git checkout master
```

## Tips

1. **Always use `--force-with-lease`** instead of `--force`
2. **Fetch before rebasing** to ensure you have latest changes
3. **Commit often** with small, focused commits
4. **Use conventional commits** for clear history
5. **Rebase before pushing** to keep history clean
6. **Check status** before committing: `git status`
7. **Review changes** before committing: `git diff`
8. **Use stash** to save work in progress
9. **Use reflog** to recover lost commits
10. **Test before pushing** to avoid breaking CI

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Rebase](https://git-scm.com/docs/git-rebase)
- [Git Reflog](https://git-scm.com/docs/git-reflog)
- [Pre-Commit](https://pre-commit.com/)
