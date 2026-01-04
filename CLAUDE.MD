# CLAUDE.MD

## Project Overview

This is a `.github` repository that contains default community health files for the organization/user account. Files in this repository are used as defaults across all repositories in the organization that don't have their own versions.

## Repository Purpose

The `.github` repository serves as a centralized location for:
- Community health files (CODE_OF_CONDUCT.md, CONTRIBUTING.md, etc.)
- Security policies (SECURITY.md)
- Issue and pull request templates
- Workflow templates
- Profile README content

## Current Files

- **SECURITY.md**: Defines the security vulnerability disclosure process via huntr.dev

## Development Guidelines

### When Adding New Files

1. **Community Health Files**: Place standard community health files in the root directory
   - CODE_OF_CONDUCT.md
   - CONTRIBUTING.md
   - SUPPORT.md
   - GOVERNANCE.md

2. **Issue Templates**: Place in `.github/ISSUE_TEMPLATE/`
   - Bug report templates
   - Feature request templates
   - Custom issue forms

3. **Pull Request Templates**: Place in `.github/`
   - PULL_REQUEST_TEMPLATE.md

4. **Workflow Templates**: Place in `.github/workflow-templates/`
   - Reusable GitHub Actions workflows

5. **Profile Content**:
   - profile/README.md for organization profile

### File Format Standards

- Use Markdown (.md) for all documentation
- Follow consistent formatting and style
- Include clear headings and sections
- Keep content concise and actionable

### Testing Changes

- Preview Markdown rendering before committing
- Verify links are working
- Ensure templates display correctly in GitHub UI

### Commit Guidelines

- Use clear, descriptive commit messages
- Follow conventional commits format when appropriate
- Group related changes together

## Working with Claude

### Preferred Workflow

1. Always check for existing files before creating new ones
2. Maintain consistency with existing file styles
3. Follow GitHub's community health file best practices
4. Test Markdown rendering and formatting

### Important Notes

- Files here apply as defaults across all repositories
- Individual repositories can override these defaults
- Changes affect the entire organization/user account
- Security-related files should be reviewed carefully

## Resources

- [GitHub Community Health Files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
