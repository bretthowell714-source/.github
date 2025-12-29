# .github Repository

This repository contains default GitHub community health files and development configurations for all repositories under this account.

## 📋 What's Included

### Community Health Files
- **SECURITY.md** - Security policy and vulnerability reporting
- **CLAUDE.MD** - AI-assisted development guide for Claude Code

### Issue Templates
- **Bug Report** - Structured bug reporting template
- **Feature Request** - Feature proposal template
- **Config** - Issue template configuration

### Pull Request Template
Comprehensive PR template with:
- Change description and type
- Testing checklist
- AI-assisted development tracking
- Review guidelines

### GitHub Actions Workflows
- **code-quality.yml** - Automated code quality checks
- **claude-pr-review.yml** - AI-powered PR review assistance

### Development Container
Complete development environment with:
- Node.js 20
- Git and GitHub CLI
- Claude Code pre-installed
- VSCode extensions
- Common development tools

### VSCode Configuration
- **settings.json** - Editor settings and formatting rules
- **extensions.json** - Recommended extensions
- **tasks.json** - Common development tasks
- **launch.json** - Debug configurations

### Code Quality Configs
- **.editorconfig** - Consistent coding styles across editors
- **.prettierrc** - Code formatting rules
- **.markdownlint.json** - Markdown linting rules
- **.gitignore** - Common files to ignore

## 🚀 Quick Start

### For New Repositories

These configurations automatically apply to all repositories in your account. When you create a new repository:

1. The issue and PR templates will be available automatically
2. Clone the repository and open in VSCode
3. Install recommended extensions when prompted
4. Start developing with Claude Code integrated

### Using the Development Container

1. Install Docker and VSCode Remote-Containers extension
2. Open repository in VSCode
3. Click "Reopen in Container" when prompted
4. Start coding in a fully configured environment

### Starting Claude Code

From any repository terminal:
```bash
npx @anthropic-ai/claude-code@latest
```

Or use the VSCode task: `Ctrl+Shift+P` → "Run Task" → "Start Claude Code"

## 🤖 AI-Assisted Development

This repository is optimized for AI-assisted development with Claude Code:

- **CLAUDE.MD** provides context for AI assistants
- Issue templates structure information for better AI analysis
- PR templates include AI contribution tracking
- Workflows generate PR context for AI review

## 📝 Customization

To customize these defaults:

1. Clone this repository
2. Modify the templates and configurations
3. Commit and push changes
4. All your repositories will use the updated defaults

## 🔒 Security

Security vulnerabilities should be reported via our [security policy](SECURITY.md).

## 📚 Resources

- [GitHub Community Health Files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Dev Containers](https://containers.dev/)
- [VSCode Workspace](https://code.visualstudio.com/docs/editor/workspaces)

## 🛠️ Development

### Making Changes

1. Create a feature branch: `git checkout -b feature/my-change`
2. Make your changes
3. Test configurations in a sample repository
4. Commit: `git commit -m "Description of changes"`
5. Push: `git push origin feature/my-change`
6. Create a pull request

### Testing Templates

To test issue/PR templates:
1. Create a test repository
2. Go to Issues → New Issue
3. Verify templates appear correctly
4. Test the PR template by creating a test PR

## 📄 License

These configurations are provided as-is for use across your repositories.

---

**Maintained with ❤️ and AI assistance by Claude Code**
