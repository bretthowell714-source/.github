# Claude Customization Hub

A comprehensive repository for customizing and extending Claude's capabilities with custom tools, plugins, and extensions.

## Overview

This repository provides a complete framework for:
- **Custom Tools**: Create and manage custom tools for Claude
- **Capabilities**: Extend Claude's native capabilities
- **Plugins**: Develop plugins to enhance functionality
- **Extensions**: Build extensions for various Claude interfaces
- **MCP Servers**: Create Model Context Protocol servers
- **Agent Configuration**: Build and configure custom agents

## Directory Structure

```
.
├── README.md                    # This file
├── SETUP.md                     # Getting started guide
├── docs/                        # Documentation
│   ├── CAPABILITIES.md          # Built-in Claude capabilities
│   ├── TOOLS.md                 # Available tools documentation
│   ├── CUSTOM_TOOLS.md          # Guide for creating custom tools
│   ├── PLUGINS.md               # Plugin development guide
│   ├── EXTENSIONS.md            # Extension development guide
│   └── MCP_SERVERS.md           # MCP server setup guide
├── tools/                       # Custom tool definitions
│   ├── examples/                # Example custom tools
│   │   ├── hello-world.js
│   │   └── http-client.js
│   └── templates/               # Tool templates
│       ├── javascript-tool.js.template
│       └── python-tool.py.template
├── plugins/                     # Custom plugins
│   ├── examples/
│   └── templates/
├── extensions/                  # Extensions
│   ├── examples/
│   └── templates/
├── agents/                      # Agent configurations
│   ├── examples/
│   └── templates/
├── mcp-servers/                 # MCP server implementations
│   ├── examples/
│   └── templates/
├── config/                      # Configuration files
│   ├── claude.config.json       # Main Claude configuration
│   ├── tools.config.json        # Tools configuration
│   └── env.example              # Environment variables template
├── scripts/                     # Utility scripts
│   ├── setup.sh                 # Setup script
│   └── validate.sh              # Validation script
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── CONTRIBUTING.md              # Contribution guidelines
```

## Quick Start

1. **Clone this repository**:
   ```bash
   git clone https://github.com/bretthowell714-source/claude-customization.git
   cd claude-customization
   ```

2. **Setup environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Read the documentation**:
   - Start with [SETUP.md](./SETUP.md)
   - Review [CAPABILITIES.md](./docs/CAPABILITIES.md)
   - Check [TOOLS.md](./docs/TOOLS.md)

4. **Explore examples**:
   - Browse `tools/examples/`
   - Check `plugins/examples/`
   - Review `agents/examples/`

## Built-in Tools & Capabilities

Claude has access to a comprehensive set of tools and capabilities:

### System Tools
- **Bash** - Execute shell commands
- **Read** - Read files from filesystem
- **Write** - Write files to filesystem
- **Edit** - Edit files with string replacement
- **Glob** - Find files by pattern matching
- **Grep** - Search file contents with regex
- **WebFetch** - Fetch and analyze web content
- **WebSearch** - Search the web
- **NotebookEdit** - Edit Jupyter notebook cells

### Specialized Agents
- **general-purpose** - Multi-step task execution
- **Explore** - Fast codebase exploration
- **Plan** - Software architecture and planning
- **Bash** - Command execution
- **statusline-setup** - Claude Code configuration

### Advanced Features
- **MCP Servers** - Model Context Protocol support
- **Tool Use** - Create custom tool definitions
- **System Prompts** - Customize Claude's behavior
- **Agent SDK** - Build custom agents

See [CAPABILITIES.md](./docs/CAPABILITIES.md) for full details.

## Creating Custom Tools

### JavaScript Example
```javascript
// tools/examples/my-tool.js
module.exports = {
  name: "my-tool",
  description: "Description of what this tool does",
  parameters: {
    type: "object",
    properties: {
      input: {
        type: "string",
        description: "Input parameter"
      }
    },
    required: ["input"]
  },
  execute: async (params) => {
    // Implementation here
    return { result: "output" };
  }
};
```

### Python Example
```python
# tools/examples/my-tool.py
class MyTool:
    def __init__(self):
        self.name = "my-tool"
        self.description = "Description of what this tool does"

    async def execute(self, **kwargs):
        # Implementation here
        return {"result": "output"}
```

## Available Plugins & Extensions

This repository includes templates and examples for:

- **Authentication Plugins** - Handle various auth methods
- **API Integration Plugins** - Connect to external services
- **Data Processing Extensions** - Transform data formats
- **UI Extensions** - Customize Claude Code interface
- **Custom Agents** - Build specialized agents for specific tasks

## Configuration

All configuration is managed through JSON files:

- `config/claude.config.json` - Main configuration
- `config/tools.config.json` - Tools configuration
- `.env` - Environment variables

See `config/` directory for detailed configuration options.

## Contributing

This is your personal customization repository! Feel free to:
- Add custom tools and plugins
- Modify configurations
- Create new agents
- Develop extensions

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## Support & Resources

- [Claude Documentation](https://claude.ai/docs)
- [Anthropic API Docs](https://docs.anthropic.com)
- [Claude Code Guide](https://docs.anthropic.com/claude-code)
- [Agent SDK Documentation](https://docs.anthropic.com/agent-sdk)

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

**Last Updated**: January 2026
