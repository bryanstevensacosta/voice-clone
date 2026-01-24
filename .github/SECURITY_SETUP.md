# Security Features Setup

This document describes the security features that need to be enabled for this repository.

## Automated Setup (via Terraform)

The following security features are configured automatically via Terraform:

- ✅ **Dependabot vulnerability alerts** - Enabled via `vulnerability_alerts = true` in `terraform/main.tf`
- ✅ **Dependabot version updates** - Configured via `.github/dependabot.yml`

## Manual Setup Required (GitHub UI)

The following security features must be enabled manually through the GitHub repository settings:

### 1. GitHub Security Advisories

**Location**: Settings → Security → Code security and analysis → Security advisories

**Steps**:
1. Go to repository Settings
2. Navigate to "Security" section in left sidebar
3. Under "Code security and analysis", find "Private vulnerability reporting"
4. Click "Enable" to allow security researchers to privately report vulnerabilities

**Purpose**: Allows coordinated disclosure of security vulnerabilities

### 2. Secret Scanning

**Location**: Settings → Security → Code security and analysis → Secret scanning

**Steps**:
1. Go to repository Settings
2. Navigate to "Security" section in left sidebar
3. Under "Code security and analysis", find "Secret scanning"
4. Click "Enable" to scan for accidentally committed secrets

**Purpose**: Automatically detects secrets (API keys, tokens, passwords) committed to the repository

**Note**: This feature is automatically enabled for public repositories, but you should verify it's active.

### 3. Dependabot Security Updates

**Location**: Settings → Security → Code security and analysis → Dependabot security updates

**Steps**:
1. Go to repository Settings
2. Navigate to "Security" section in left sidebar
3. Under "Code security and analysis", find "Dependabot security updates"
4. Click "Enable" to automatically create PRs for security vulnerabilities

**Purpose**: Automatically creates pull requests to update dependencies with known security vulnerabilities

## Verification Checklist

After setup, verify all features are enabled:

- [ ] Dependabot vulnerability alerts - Check Settings → Security
- [ ] Dependabot version updates - Check `.github/dependabot.yml` exists
- [ ] Dependabot security updates - Check Settings → Security
- [ ] Private vulnerability reporting - Check Settings → Security
- [ ] Secret scanning - Check Settings → Security

## Additional Security Best Practices

### Branch Protection

Branch protection rules are configured via Terraform for:
- `master` branch
- `main` branch
- `develop` branch

These rules enforce:
- Required pull request reviews
- Required status checks (test, lint, type-check)
- Linear history (rebase only)
- No force pushes or deletions

### Pre-commit Hooks

Security-related pre-commit hooks are configured in `.pre-commit-config.yaml`:
- `detect-private-key` - Prevents committing private keys
- `check-added-large-files` - Prevents committing large files

### Environment Variables

Sensitive configuration should be stored in environment variables, not committed to the repository:
- Use `.env` file for local development (git-ignored)
- Use `.env.example` as a template (committed)
- Never commit API keys, tokens, or passwords

## Monitoring

### Security Alerts

GitHub will send notifications for:
- Dependabot alerts (vulnerabilities in dependencies)
- Secret scanning alerts (detected secrets)
- Security advisories (reported vulnerabilities)

Configure notification preferences in: Settings → Notifications → Security alerts

### Regular Reviews

Periodically review:
- Dependabot PRs (weekly)
- Security advisories (as they arrive)
- Secret scanning alerts (immediately)

## Resources

- [GitHub Security Features](https://docs.github.com/en/code-security)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Security Advisories](https://docs.github.com/en/code-security/security-advisories)
