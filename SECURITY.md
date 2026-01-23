# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

**Note**: As this project is in early development (pre-1.0), we currently only support the latest minor version. Once we reach 1.0, we will maintain security updates for multiple versions.

## Reporting a Vulnerability

We take the security of Voice Clone CLI seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not

- **Do not** open a public GitHub issue for security vulnerabilities
- **Do not** disclose the vulnerability publicly until it has been addressed
- **Do not** exploit the vulnerability beyond what is necessary to demonstrate it

### How to Report

**Email**: bryanstevensacosta@gmail.com

Please include the following information in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Suggested fix** (if you have one)
5. **Your contact information** for follow-up

### Example Report

```
Subject: [SECURITY] Potential Path Traversal in Audio File Loading

Description:
The audio file loading function does not properly sanitize file paths,
potentially allowing access to files outside the intended directory.

Steps to Reproduce:
1. Run: voice-clone train --samples "../../../etc/passwd"
2. Observe that the system attempts to read files outside the data directory

Impact:
An attacker could potentially read arbitrary files on the system.

Suggested Fix:
Validate and sanitize all file paths using os.path.abspath() and ensure
they are within the expected directory structure.

Contact: security-researcher@example.com
```

## Response Timeline

- **Initial Response**: Within 48 hours of receiving your report
- **Status Update**: Within 7 days with our assessment and planned actions
- **Fix Timeline**: Depends on severity and complexity
  - **Critical**: Within 7 days
  - **High**: Within 30 days
  - **Medium**: Within 90 days
  - **Low**: Next regular release

## Security Update Process

When a security vulnerability is confirmed:

1. **Acknowledgment**: We will acknowledge receipt of your report
2. **Investigation**: We will investigate and confirm the vulnerability
3. **Fix Development**: We will develop and test a fix
4. **Disclosure**: We will coordinate disclosure with you
5. **Release**: We will release a security update
6. **Announcement**: We will publish a security advisory

## Security Best Practices

When using Voice Clone CLI, follow these security best practices:

### Data Privacy

- **Voice Samples**: Store voice samples securely and obtain proper consent
- **Personal Data**: Never commit personal data or voice samples to version control
- **Access Control**: Restrict access to trained models and audio samples
- **Data Retention**: Delete voice samples and models when no longer needed

### Configuration Security

- **Environment Variables**: Use `.env` files for sensitive configuration (never commit)
- **API Keys**: Store API keys securely using environment variables or secret management
- **File Permissions**: Set appropriate file permissions on data directories
- **Config Files**: Keep `config/config.yaml` out of version control

### Deployment Security

- **Dependencies**: Keep dependencies up to date
- **Virtual Environment**: Always use virtual environments
- **Input Validation**: Validate all user inputs
- **Error Messages**: Don't expose sensitive information in error messages

### Example Secure Configuration

```bash
# .env file (never commit this)
MODEL_PATH=/secure/path/to/models
API_KEY=your-secret-api-key
MAX_AUDIO_SIZE=10485760  # 10MB limit
```

```yaml
# config/config.yaml (gitignored)
security:
  max_file_size: 10485760  # 10MB
  allowed_extensions: ['.wav', '.mp3', '.flac']
  sanitize_paths: true
  validate_audio: true
```

## Known Security Considerations

### Voice Cloning Ethics

Voice cloning technology can be misused. Users must:

- **Obtain Consent**: Get explicit permission before cloning someone's voice
- **Respect Rights**: Respect intellectual property and personality rights
- **Prevent Misuse**: Don't use cloned voices for fraud, impersonation, or deception
- **Legal Compliance**: Follow all applicable laws and regulations

### Audio File Processing

- **File Size Limits**: Large audio files can cause memory issues
- **Format Validation**: Only process supported audio formats
- **Malicious Files**: Validate audio files before processing
- **Resource Limits**: Set appropriate resource limits to prevent DoS

### Model Security

- **Model Integrity**: Verify model files haven't been tampered with
- **Model Storage**: Store trained models securely
- **Model Sharing**: Be cautious when sharing or downloading models
- **Access Control**: Restrict access to sensitive models

## Security Tools

This project uses several security tools:

- **pre-commit hooks**: Detect secrets and security issues before commit
- **Dependabot**: Automated dependency updates for security patches
- **GitHub Security Advisories**: Vulnerability tracking and disclosure
- **Secret Scanning**: Detect accidentally committed secrets

## Vulnerability Disclosure Policy

We follow responsible disclosure practices:

1. **Private Disclosure**: Report vulnerabilities privately first
2. **Coordination**: We will work with you on disclosure timing
3. **Credit**: We will credit you in the security advisory (if desired)
4. **Public Disclosure**: After fix is released and users have time to update

## Security Hall of Fame

We recognize security researchers who help improve our security:

<!-- Security researchers will be listed here -->

*No security vulnerabilities have been reported yet.*

## Questions?

If you have questions about this security policy, please contact:

- **Email**: bryanstevensacosta@gmail.com
- **GitHub Discussions**: [Security Category](https://github.com/yourusername/voice-clone-cli/discussions/categories/security)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Responsible Disclosure Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)

---

**Last Updated**: January 23, 2026

Thank you for helping keep Voice Clone CLI and its users safe!
