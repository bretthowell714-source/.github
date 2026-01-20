# Setup Guide

Complete guide to setting up your Claude customization environment.

## Prerequisites

- Node.js 18+ (for JavaScript tools)
- Python 3.8+ (for Python tools)
- Git
- Claude API key (for API-based customizations)
- Git CLI (for GitHub integration)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/bretthowell714-source/claude-customization.git
cd claude-customization
```

### 2. Install Dependencies

```bash
# For Node.js tools
npm install

# For Python tools (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# API Keys
ANTHROPIC_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here

# Claude Code Configuration
CLAUDE_CODE_MODEL=claude-opus-4-5-20251101
CLAUDE_CODE_CLI_VERSION=latest

# Custom Tool Settings
ENABLE_CUSTOM_TOOLS=true
TOOL_TIMEOUT=30000
MAX_RETRIES=3

# MCP Server Configuration
MCP_SERVER_PORT=8000
MCP_ENABLE_EXPERIMENTAL=false
```

### 4. Validate Setup

```bash
bash scripts/validate.sh
```

This will check:
- Node.js and Python installations
- Required API keys
- Directory structure
- File permissions

### 5. Explore Examples

Check out the example implementations:

```bash
# List available tools
ls tools/examples/

# List available plugins
ls plugins/examples/

# List available agents
ls agents/examples/
```

## Project Structure Overview

### Core Directories

- **tools/** - Custom tool implementations
- **plugins/** - Plugin code for extending functionality
- **extensions/** - Browser/IDE extensions
- **agents/** - Custom agent configurations
- **mcp-servers/** - MCP server implementations
- **config/** - Configuration files
- **docs/** - Documentation
- **scripts/** - Utility scripts

### Configuration Files

- `config/claude.config.json` - Main Claude configuration
- `config/tools.config.json` - Tools setup and registration
- `.env` - Environment variables (local, not in git)
- `package.json` - Node.js dependencies
- `requirements.txt` - Python dependencies

## Creating Your First Custom Tool

### JavaScript

1. Create a new file in `tools/custom/my-first-tool.js`:

```javascript
module.exports = {
  name: "my-first-tool",
  description: "My first custom Claude tool",
  parameters: {
    type: "object",
    properties: {
      message: {
        type: "string",
        description: "Message to process"
      }
    },
    required: ["message"]
  },
  execute: async (params) => {
    const processed = params.message.toUpperCase();
    return {
      success: true,
      original: params.message,
      processed: processed
    };
  }
};
```

2. Register it in `config/tools.config.json`:

```json
{
  "tools": [
    {
      "name": "my-first-tool",
      "path": "./tools/custom/my-first-tool.js",
      "enabled": true
    }
  ]
}
```

3. Use it in Claude:

```
I have a tool called "my-first-tool". Please use it with the message "hello world".
```

### Python

1. Create `tools/custom/my_first_tool.py`:

```python
class MyFirstTool:
    def __init__(self):
        self.name = "my-first-tool-py"
        self.description = "My first Python tool"
        self.parameters = {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to process"
                }
            },
            "required": ["message"]
        }

    async def execute(self, message: str, **kwargs):
        processed = message.upper()
        return {
            "success": True,
            "original": message,
            "processed": processed
        }
```

## Setting Up Claude Code Integration

1. **Install Claude Code CLI**:

```bash
npm install -g @anthropic-ai/claude-code
```

2. **Configure for this repository**:

```bash
claude-code config set workspace $(pwd)
```

3. **Enable custom tools**:

```bash
claude-code config set customToolsPath ./tools/custom
```

## Setting Up Custom Agents

1. Create agent config in `agents/my-agent.json`:

```json
{
  "name": "my-agent",
  "description": "My custom agent",
  "model": "claude-opus-4-5-20251101",
  "tools": ["my-first-tool"],
  "systemPrompt": "You are a helpful assistant with access to custom tools.",
  "temperature": 0.7,
  "maxTokens": 4096
}
```

2. Use it:

```bash
claude-code agent run agents/my-agent.json
```

## Using MCP Servers

1. Create MCP server in `mcp-servers/my-server.js`:

```javascript
const MCPServer = require("@anthropic-ai/mcp-server");

const server = new MCPServer({
  name: "my-mcp-server",
  version: "1.0.0"
});

server.tool("example-tool", {
  description: "Example MCP tool",
  inputSchema: {
    type: "object",
    properties: {
      input: { type: "string" }
    }
  }
}, async (input) => {
  return { result: input.toUpperCase() };
});

server.start();
```

2. Configure in `.env`:

```env
MCP_SERVERS=./mcp-servers/my-server.js
```

3. Start the server:

```bash
npm start
```

## Troubleshooting

### Tools not loading

1. Check `config/tools.config.json` for syntax errors
2. Verify file paths are correct
3. Check file permissions: `chmod +x tools/custom/*.js`
4. Review logs: `tail -f logs/tools.log`

### Environment variables not loading

1. Ensure `.env` file exists in project root
2. Check `.env` is not listed in `.gitignore`
3. Source the environment: `source .env`

### API key issues

1. Verify `ANTHROPIC_API_KEY` is set correctly
2. Check for trailing whitespace in `.env`
3. Test API access: `npm run test-api`

### Port conflicts with MCP server

1. Check if port 8000 is in use: `lsof -i :8000`
2. Change port in `.env`: `MCP_SERVER_PORT=8001`

## Next Steps

1. Read [CAPABILITIES.md](./docs/CAPABILITIES.md) to understand Claude's features
2. Review [TOOLS.md](./docs/TOOLS.md) for available tools
3. Check [CUSTOM_TOOLS.md](./docs/CUSTOM_TOOLS.md) for advanced tool development
4. Explore plugin development in [PLUGINS.md](./docs/PLUGINS.md)
5. Build custom agents with [Agent SDK](https://docs.anthropic.com/agent-sdk)

## Getting Help

- Check documentation in `docs/` directory
- Review examples in `tools/examples/`, `plugins/examples/`
- Check logs in `logs/` directory
- See GitHub issues for common problems

---

Happy customizing! 🚀
