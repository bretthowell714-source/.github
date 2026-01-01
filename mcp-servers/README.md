# MCP Servers - Model Context Protocol Integrations

Complete MCP server implementations for Claude integrations across all platforms.

## 🚀 Available MCP Servers

### 1. Claude Files API Server
**Location**: `file-upload-mcp/server.py`

**Tools Provided**:
- `upload_file` - Upload files to Anthropic Files API
- `list_files` - List all uploaded files
- `delete_file` - Delete files

### 2. Meta-Skill Engine Server
**Location**: `meta-skill-mcp/server.py`

**Tools Provided**:
- `embed_skill` - Add new skills to the system
- `get_recommendations` - Get skill recommendations
- `record_learning` - Record learned knowledge
- `generate_report` - Generate system reports
- `export_config` - Export configuration

## 📦 Installation

### Prerequisites
```bash
pip install mcp anthropic requests pyyaml
```

### Test Servers
```bash
# Test file upload MCP server
python3 file-upload-mcp/server.py

# Test meta-skill MCP server
python3 meta-skill-mcp/server.py
```

## 🖥️ Platform Configurations

### Claude Desktop (Windows/Mac/Linux)

**Config Location**:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Setup**:
```bash
# Copy the config
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"
```

### VSCode

**Config Location**: `.vscode/mcp_settings.json`

**Setup**:
```bash
# Copy to your project
cp vscode_config.json /path/to/your/project/.vscode/mcp_settings.json
```

### Docker

See `../docker/` for containerized MCP servers.

### Android

See `../android/` for mobile integration.

## 🔧 Configuration Guide

### Environment Variables

Create `.env` file:
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional
GITHUB_TOKEN=ghp_xxxxx
BRAVE_API_KEY=xxxxx
```

### Custom MCP Server

Create your own MCP server:

```python
#!/usr/bin/env python3
from mcp.server import Server
import mcp.server.stdio
import mcp.types as types

server = Server("my-custom-server")

@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="my_tool",
            description="Does something cool",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        return [types.TextContent(
            type="text",
            text=f"Result: {arguments['param']}"
        )]

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, ...)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

Add to config:
```json
{
  "mcpServers": {
    "my-custom-server": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## 🌐 Official MCP Servers

### Pre-built Servers (via npm)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {"SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"}
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {"DATABASE_URL": "${DATABASE_URL}"}
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

## 🔍 Testing Your Setup

### Verify MCP Server is Running

```bash
# Check if server starts
python3 file-upload-mcp/server.py &
PID=$!

# Send test request (MCP uses stdio)
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 file-upload-mcp/server.py

kill $PID
```

### Test in Claude Desktop

1. Add server to config
2. Restart Claude Desktop
3. Look for new tools in tool picker
4. Test a tool

## 📱 Platform-Specific Guides

### Windows Setup
```powershell
# Set API key
$env:ANTHROPIC_API_KEY = "your-key"

# Copy config
Copy-Item claude_desktop_config.json $env:APPDATA\Claude\
```

### macOS Setup
```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Copy config
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/

# Restart Claude
killall Claude && open -a Claude
```

### Linux Setup
```bash
# Set API key
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# Copy config
mkdir -p ~/.config/Claude
cp claude_desktop_config.json ~/.config/Claude/
```

## 🐳 Docker Deployment

See `../docker/mcp-servers/` for containerized deployments.

## 📊 Monitoring & Debugging

### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Server Logs

Claude Desktop logs:
- **Windows**: `%APPDATA%\Claude\logs`
- **macOS**: `~/Library/Logs/Claude`
- **Linux**: `~/.config/Claude/logs`

## 🔐 Security

- **NEVER** commit API keys
- Use environment variables
- Validate all inputs
- Sanitize file paths
- Limit file sizes

## 🚀 Advanced Features

### Multi-Server Chaining

Servers can call other servers:

```python
# Server A calls Server B
@server.call_tool()
async def call_tool(name, args):
    if name == "complex_task":
        # Call another MCP server
        result1 = await call_mcp_server("server-b", "tool1", {})
        result2 = await call_mcp_server("server-c", "tool2", {})
        return combine_results(result1, result2)
```

### State Management

```python
class StatefulMCPServer:
    def __init__(self):
        self.state = {}
        self.server = Server("stateful")

    @self.server.call_tool()
    async def call_tool(self, name, args):
        # Access state
        self.state[name] = args
        return [types.TextContent(text=f"State updated")]
```

## 📚 Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/anthropics/mcp-python-sdk)
- [Official MCP Servers](https://github.com/anthropics/mcp-servers)
- [Claude Desktop Docs](https://docs.anthropic.com/claude/desktop)

## 🆘 Troubleshooting

### Server Not Appearing

1. Check config file location
2. Verify JSON syntax
3. Check file permissions
4. Restart Claude Desktop
5. Check logs

### Tools Not Working

1. Verify API keys set
2. Check network connectivity
3. Enable debug logging
4. Test server standalone

### Performance Issues

1. Reduce tool complexity
2. Cache results
3. Use async operations
4. Limit data returned

---

**Ready to supercharge Claude with custom tools!** 🚀
