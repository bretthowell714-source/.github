# Claude AI Development Guide

This document provides context and guidelines for AI-assisted development in this repository.

## Repository Overview

This is a `.github` repository containing GitHub-specific configurations and documentation. The repository includes:

- Security policies and vulnerability reporting procedures
- GitHub Actions workflows (if applicable)
- Issue and PR templates
- Community health files

## Development Guidelines

### File Naming Conventions

- Use UPPERCASE for special GitHub files (e.g., `SECURITY.md`, `CLAUDE.MD`)
- Use lowercase with hyphens for workflow files (e.g., `ci-workflow.yml`)
- Be consistent with existing naming patterns in the repository

### Code Style

- Use clear, descriptive file names
- Follow Markdown best practices for documentation
- Keep documentation concise but comprehensive
- Use proper heading hierarchy

### Git Workflow

- Create feature branches for all changes
- Use descriptive commit messages
- Follow conventional commit format when possible
- Always test changes before committing

### Security Considerations

- Never commit sensitive information (tokens, credentials, API keys)
- Review security implications of workflow changes
- Follow the vulnerability reporting process outlined in SECURITY.md
- Validate all external inputs in GitHub Actions

## Common Tasks

### Adding GitHub Actions Workflows

1. Create workflow files in `.github/workflows/`
2. Use descriptive names (e.g., `ci.yml`, `deploy.yml`)
3. Test workflows thoroughly before merging
4. Document required secrets in README or workflow comments

### Updating Documentation

1. Keep SECURITY.md current with reporting procedures
2. Update this CLAUDE.MD as the project evolves
3. Ensure all links are valid and up-to-date

### Creating Issue Templates

1. Place templates in `.github/ISSUE_TEMPLATE/`
2. Use YAML frontmatter for configuration
3. Provide clear guidance for users

## Testing

- Test GitHub Actions workflows using `act` or branch deployments
- Validate Markdown syntax using linters
- Review rendered documentation on GitHub

## AI-Specific Instructions

### When Making Changes

- Always read existing files before modifying them
- Maintain consistency with existing patterns
- Ask for clarification on ambiguous requirements
- Consider security implications of all changes

### GitHub Actions Context

- Be aware of GitHub Actions syntax and limitations
- Use officially supported actions when possible
- Document required repository secrets
- Consider workflow security best practices

### Documentation Standards

- Use clear, professional language
- Include examples where helpful
- Keep formatting consistent
- Update table of contents when needed

## Project Structure

```
.github/
├── SECURITY.md          # Security vulnerability reporting
├── CLAUDE.MD           # This file - AI development guide
├── workflows/          # GitHub Actions workflows (if any)
├── ISSUE_TEMPLATE/     # Issue templates (if any)
└── PULL_REQUEST_TEMPLATE/ # PR templates (if any)
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Community Health Files](https://docs.github.com/en/communities)
- [Markdown Guide](https://www.markdownguide.org/)

## Notes for AI Assistants

- This repository contains GitHub configuration files
- Security is paramount - be cautious with workflow permissions
- Test all changes thoroughly
- Maintain backward compatibility when possible
- Follow GitHub's recommended practices for community health files

---

Last Updated: 2025-12-28
