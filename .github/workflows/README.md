# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD and automation.

## Workflows

### 1. CI (ci.yml)

**Purpose**: Run continuous integration checks (lint, type-check, test)

**Triggers**:
- Push to `master`, `main`, or `develop` branches
- Pull requests to `master`, `main`, or `develop` branches
- Pull request reviews (when approval is submitted)

**Special Behavior**:

#### For PRs from @bryanstevensacosta (owner)
- ✅ CI runs immediately without waiting for approval
- ✅ Auto-approved by the auto-approve workflow
- ✅ No delays or waiting

#### For PRs from other contributors
- ⏳ CI waits for at least 1 approval before running
- 💬 Bot comments on PR explaining the wait
- ✅ Once approved, CI runs automatically
- 🔄 CI re-runs when new commits are pushed (if still approved)

**Jobs**:
1. **check-approval**: Determines if CI should run
   - Checks if PR author is the owner
   - Checks if PR has at least 1 approval
   - Outputs decision for other jobs

2. **lint**: Code formatting and linting
   - Black formatting check
   - Ruff linting
   - Runs on Python 3.9, 3.10, 3.11

3. **type-check**: Type checking with MyPy
   - Runs on Python 3.9, 3.10, 3.11

4. **test**: Test suite with coverage
   - pytest with coverage reporting
   - Uploads coverage to Codecov
   - Runs on Python 3.9, 3.10, 3.11

5. **waiting-for-approval**: Notification job
   - Only runs when CI is waiting for approval
   - Comments on PR to inform contributors

### 2. Auto Approve (auto-approve.yml)

**Purpose**: Automatically approve PRs from the repository owner

**Triggers**:
- Pull request opened
- Pull request synchronized (new commits)
- Pull request reopened

**Behavior**:
- Only runs for PRs from @bryanstevensacosta
- Automatically approves the PR
- Adds a comment indicating auto-approval
- Allows owner's PRs to bypass the 1-approval requirement

**Permissions Required**:
- `pull-requests: write`

### 3. Auto Update PRs (auto-update-pr.yml)

**Purpose**: Automatically update open PRs with latest changes from base branch

**Triggers**:
- Push to `master`, `main`, or `develop` branches
- Manual trigger via `workflow_dispatch`

**Behavior**:

#### Update Policy
Only updates PRs that meet ONE of these conditions:
- ✅ PR is from @bryanstevensacosta (owner)
- ✅ PR has at least 1 approval

#### What it does
1. Detects when base branch (master/main/develop) is updated
2. Finds all open PRs targeting that branch
3. For each eligible PR:
   - Checks if it's from owner OR has approval
   - Skips if neither condition is met
   - Checks if PR is behind base branch
   - Updates the branch automatically (rebase)
   - Adds comment explaining the update
   - If conflicts exist, comments with manual instructions

#### Notifications
- ✅ **Success**: Comments with update details
- ⚠️ **Conflicts**: Comments with manual resolution steps
- ⏭️ **Skipped**: Logged but no comment (waiting for approval)

**Permissions Required**:
- `contents: write`
- `pull-requests: write`

## Configuration

### Owner Username

The owner username is hardcoded in both workflows:
- `ci.yml`: Line with `const owner = 'bryanstevensacosta';`
- `auto-approve.yml`: Line with `if: github.event.pull_request.user.login == 'bryanstevensacosta'`

To change the owner, update both files.

### Approval Requirements

The approval logic is in `ci.yml` in the `check-approval` job:

```javascript
// Check if PR has at least one approval
const reviews = await github.rest.pulls.listReviews({
  owner: context.repo.owner,
  repo: context.repo.repo,
  pull_number: context.payload.pull_request.number
});

const hasApproval = reviews.data.some(review => review.state === 'APPROVED');
```

## Workflow Diagram

### Owner's PR Flow
```
PR Created (by @bryanstevensacosta)
    ↓
Auto-Approve Workflow
    ↓
PR Approved ✅
    ↓
CI Workflow (check-approval)
    ↓
Owner detected → CI runs immediately
    ↓
lint, type-check, test (all run in parallel)
    ↓
All checks pass ✅
    ↓
Ready to merge
```

### Contributor's PR Flow
```
PR Created (by contributor)
    ↓
CI Workflow (check-approval)
    ↓
No approval yet → CI waits ⏳
    ↓
Bot comments: "Waiting for approval"
    ↓
Reviewer approves PR ✅
    ↓
pull_request_review event triggers CI
    ↓
lint, type-check, test (all run in parallel)
    ↓
All checks pass ✅
    ↓
Ready to merge
```

## Testing the Workflows

### Test Owner's PR
```bash
# 1. Create a branch as owner
git checkout -b test/owner-pr

# 2. Make a change
echo "test" >> test.txt
git add test.txt
git commit -m "test: owner PR"

# 3. Push and create PR
git push origin test/owner-pr

# Expected:
# - Auto-approve workflow runs and approves
# - CI runs immediately
# - PR is ready to merge once CI passes
```

### Test Contributor's PR
```bash
# 1. Have a contributor create a PR
# (or simulate by creating PR from a different account)

# Expected:
# - CI does not run initially
# - Bot comments: "Waiting for approval"
# - After approval, CI runs automatically
```

### Test Auto-Update (Owner's PR)
```bash
# 1. Create and merge a PR to master
git checkout master
git pull origin master
git checkout -b feature/update-test
echo "update" >> test.txt
git add test.txt
git commit -m "feat: trigger auto-update"
git push origin feature/update-test
# Create and merge PR

# 2. Create another PR from owner (don't merge yet)
git checkout -b feature/will-be-updated
echo "another change" >> test2.txt
git add test2.txt
git commit -m "feat: will be auto-updated"
git push origin feature/will-be-updated
# Create PR

# Expected after merging first PR:
# - Auto-update workflow triggers
# - Second PR is automatically updated
# - Comment added to second PR
```

### Test Auto-Update (Contributor's PR)
```bash
# 1. Contributor creates PR (not approved yet)
# 2. Merge another PR to master
# Expected:
# - Auto-update workflow triggers
# - Contributor's PR is NOT updated (no approval)
# - No comment added

# 3. Approve contributor's PR
# 4. Merge another PR to master
# Expected:
# - Auto-update workflow triggers
# - Contributor's PR IS updated (has approval)
# - Comment added
```

## Troubleshooting

### CI not running for owner's PRs

**Check**:
1. Username is correct in both workflows
2. Workflow files are on the target branch (master/main)
3. GitHub Actions are enabled for the repository

**Debug**:
```bash
# Check workflow runs
gh run list --workflow=ci.yml

# View specific run
gh run view <run-id>
```

### Auto-approve not working

**Check**:
1. Workflow has `pull-requests: write` permission
2. `GITHUB_TOKEN` has sufficient permissions
3. Repository settings allow GitHub Actions to approve PRs

**Fix**:
- Go to Settings → Actions → General
- Under "Workflow permissions", select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### CI running before approval for contributors

**Check**:
1. The `check-approval` job logic
2. Review state is actually "APPROVED"
3. No race conditions with approval timing

**Debug**:
Add logging to the check-approval step:
```javascript
console.log('Reviews:', JSON.stringify(reviews.data, null, 2));
```

## Security Considerations

### pull_request_target vs pull_request

The auto-approve workflow uses `pull_request_target` instead of `pull_request`:
- `pull_request_target` runs in the context of the base branch
- Has access to secrets and write permissions
- Safe because it only runs for the owner (hardcoded check)

### Token Permissions

Both workflows use `GITHUB_TOKEN` with minimal required permissions:
- `ci.yml`: Read access (default)
- `auto-approve.yml`: `pull-requests: write` (explicit)

## Maintenance

### Updating Python Versions

To add/remove Python versions, update the matrix in `ci.yml`:

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]  # Add 3.12
```

Also update Terraform's `main.tf` to match:
```hcl
contexts = [
  "lint (3.9)",
  "lint (3.10)",
  "lint (3.11)",
  "lint (3.12)",  # Add this
  # ... etc
]
```

### Changing Approval Requirements

To require more approvals, update `ci.yml`:

```javascript
// Change from 1 to 2 approvals
const approvalCount = reviews.data.filter(r => r.state === 'APPROVED').length;
const hasApproval = approvalCount >= 2;
```

Also update Terraform's `main.tf`:
```hcl
required_approving_review_count = 2
```

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Script Action](https://github.com/actions/github-script)
- [Auto Approve Action](https://github.com/hmarr/auto-approve-action)
