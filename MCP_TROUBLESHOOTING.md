# MCP Server Troubleshooting Guide

## Problem Summary

The Playwright, Puppeteer, and Selenium MCP servers were not working for Claude Desktop/Code. This guide documents the issues found and the solutions implemented.

## Root Cause Analysis

### Issues Identified

1. **MCP Servers Not Installed**
   - Playwright MCP server (@playwright/mcp) was not installed globally
   - Puppeteer MCP server (@modelcontextprotocol/server-puppeteer) was not installed
   - Selenium MCP server (selenium-mcp-server) was not installed

2. **MCP Configuration Missing**
   - The `.claude.json` configuration file had an empty `mcpServers` object
   - No MCP servers were registered for the current project

3. **Server Paths Not Configured**
   - Even with global Playwright installed, the MCP wrapper was not configured
   - No command/args specified for launching the MCP servers

## Solutions Implemented

### 1. Install MCP Servers

#### Playwright MCP Server
```bash
npm install -g @playwright/mcp
```

**Installed Version:** @playwright/mcp@0.0.54
**Binary Location:** /opt/node22/bin/mcp-server-playwright
**Documentation:** https://github.com/microsoft/playwright-mcp

#### Puppeteer MCP Server
```bash
# No installation needed - uses npx to run on demand
npx -y @modelcontextprotocol/server-puppeteer
```

**Package:** @modelcontextprotocol/server-puppeteer
**Official Anthropic Package:** Yes
**Documentation:** https://www.npmjs.com/package/@modelcontextprotocol/server-puppeteer

#### Selenium MCP Server
```bash
pip install selenium-mcp-server
```

**Installed Version:** selenium-mcp-server-1.2.0
**Binary Location:** /usr/local/bin/selenium-mcp-server
**Documentation:** https://pypi.org/project/selenium-mcp-server/

### 2. Configure MCP Servers in Claude

Updated `~/.claude.json` to include the MCP server configurations:

```json
{
  "projects": {
    "/home/user/.github": {
      "mcpServers": {
        "playwright": {
          "command": "npx",
          "args": ["@playwright/mcp@latest"]
        },
        "puppeteer": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
        },
        "selenium": {
          "command": "selenium-mcp-server",
          "args": []
        }
      }
    }
  }
}
```

## Server Details

### Playwright MCP Server

**What It Provides:**
- Browser automation using Playwright's accessibility tree
- Structured accessibility snapshots (no screenshots needed)
- Support for Chromium, Firefox, and WebKit
- LLM-friendly structured data instead of pixel-based input

**Key Features:**
- Fast and lightweight
- Deterministic tool application
- No vision models required
- Works with Claude Desktop, VS Code, Cursor, and other MCP clients

**Configuration Options:**
```json
{
  "playwright": {
    "command": "npx",
    "args": [
      "@playwright/mcp@latest",
      "--allowed-origins", "https://example.com",
      "--blocked-origins", "https://ads.example.com"
    ]
  }
}
```

**Available Command Options:**
- `--allowed-hosts`: Comma-separated list of allowed hosts
- `--allowed-origins`: Semicolon-separated list of trusted origins
- `--blocked-origins`: Semicolon-separated list of blocked origins

### Puppeteer MCP Server

**What It Provides:**
- Browser automation using Puppeteer
- Web scraping and interaction capabilities
- Screenshot capture (full page or elements)
- Console log monitoring
- JavaScript execution in browser context

**Key Features:**
- AI Vision Integration
- Automatic cookie and CAPTCHA handling
- Headless browser control
- Element interaction and form filling

**Configuration:**
```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
  }
}
```

### Selenium MCP Server

**What It Provides:**
- Browser automation via Selenium WebDriver
- Cross-browser testing support (Chrome, Firefox, Edge, Safari)
- Web element interaction
- Form automation and testing
- Screenshot capture

**Key Features:**
- Integration with AI assistants like Claude
- Natural language command support
- Automated testing capabilities
- Support for multiple implementations (Python, JavaScript, Java)

**Configuration:**
```json
{
  "selenium": {
    "command": "selenium-mcp-server",
    "args": []
  }
}
```

**Python Implementation Details:**
- Requires: Python 3.11+
- Dependencies: selenium, webdriver-manager, mcp
- WebDriver auto-download via webdriver-manager

## Verification Steps

### 1. Check Installation

```bash
# Check Playwright MCP
which mcp-server-playwright
mcp-server-playwright --version

# Check Puppeteer MCP (via npx)
npx @modelcontextprotocol/server-puppeteer --version

# Check Selenium MCP
which selenium-mcp-server
selenium-mcp-server --version
```

### 2. Verify Configuration

```bash
# View Claude configuration
cat ~/.claude.json | grep -A30 "mcpServers"

# Check for proper JSON formatting
cat ~/.claude.json | jq '.projects[].mcpServers'
```

### 3. Test MCP Server Connectivity

To test if the MCP servers are working:

1. **Restart Claude Code/Desktop**
   - Close and reopen Claude to reload the configuration

2. **Check Available Tools**
   - In a new Claude session, the MCP server tools should be available
   - Look for tools prefixed with `mcp__playwright__`, `mcp__puppeteer__`, `mcp__selenium__`

3. **Try a Simple Command**
   ```
   Use the playwright MCP server to navigate to https://example.com
   and get the page title
   ```

## Common Issues and Solutions

### Issue: "MCP server not found"

**Solution:**
1. Verify the server is installed:
   ```bash
   npm list -g @playwright/mcp
   pip list | grep selenium-mcp-server
   ```
2. Check the command path in configuration
3. Restart Claude Code/Desktop

### Issue: "Command not found: mcp-server-playwright"

**Solution:**
```bash
# Reinstall the package
npm uninstall -g @playwright/mcp
npm install -g @playwright/mcp

# Verify binary exists
ls -la /opt/node22/bin/mcp-server-playwright
```

### Issue: "npx command fails"

**Solution:**
1. Verify Node.js and npx are installed:
   ```bash
   node --version
   npx --version
   ```
2. Try running manually:
   ```bash
   npx @playwright/mcp@latest --version
   ```

### Issue: "Selenium MCP server crashes"

**Solution:**
1. Check Python version (requires 3.11+):
   ```bash
   python3 --version
   ```
2. Reinstall with dependencies:
   ```bash
   pip uninstall selenium-mcp-server
   pip install selenium-mcp-server
   ```
3. Verify webdriver installation:
   ```bash
   python3 -c "from selenium import webdriver; print('OK')"
   ```

### Issue: "MCP server configuration not loading"

**Solution:**
1. Check JSON syntax:
   ```bash
   cat ~/.claude.json | jq .
   ```
2. Ensure proper project path in configuration
3. Check file permissions:
   ```bash
   ls -la ~/.claude.json
   chmod 600 ~/.claude.json
   ```

## Alternative Configuration Methods

### Method 1: Using Claude CLI (Preferred)

```bash
# Add servers using Claude CLI
claude mcp add playwright npx @playwright/mcp@latest
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer -- -y
claude mcp add selenium selenium-mcp-server

# List configured servers
claude mcp list

# Remove a server
claude mcp remove playwright
```

### Method 2: Manual JSON Editing

Edit `~/.claude.json` directly with your preferred text editor:

```json
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "server-name": {
          "command": "command-to-run",
          "args": ["arg1", "arg2"]
        }
      }
    }
  }
}
```

### Method 3: Project-Specific Configuration

Create a `.claude/mcp.json` file in your project:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Resources

### Official Documentation

- **Playwright MCP:** https://github.com/microsoft/playwright-mcp
- **Puppeteer MCP:** https://www.npmjs.com/package/@modelcontextprotocol/server-puppeteer
- **Selenium MCP:** https://pypi.org/project/selenium-mcp-server/
- **MCP Protocol:** https://modelcontextprotocol.io

### Community Resources

- **MCP Server Directory:** https://mcpservers.org
- **Awesome MCP Servers:** https://github.com/punkpeye/awesome-mcp-servers
- **MCP Marketplace:** https://mcpmarket.com

### Tutorials and Guides

- **Playwright MCP Tutorial:** https://autify.com/blog/playwright-mcp
- **Supercharging Selenium with MCP:** https://anandhik.medium.com/supercharging-selenium-with-mcp-server-and-claude-ai-42d7e269555a
- **Top MCP Servers for Test Automation:** https://testguild.com/top-model-context-protocols-mcp/

## System Information

**Environment Details:**
- **OS:** Linux 4.4.0
- **Node.js:** v22.21.1
- **Python:** 3.11.14
- **NPM:** Latest
- **Claude Code:** Current version

**Installation Locations:**
- **Node modules:** /opt/node22/lib/node_modules
- **Python packages:** /usr/local/lib/python3.11/site-packages
- **Binaries:** /opt/node22/bin, /usr/local/bin
- **Config:** ~/.claude.json

## Next Steps

1. **Restart Claude Code/Desktop** to load the new MCP server configurations
2. **Test each MCP server** with simple commands
3. **Review MCP server logs** if issues persist
4. **Consult official documentation** for advanced features
5. **Join community forums** for support and tips

## Changelog

### 2026-01-04
- Installed Playwright MCP server (@playwright/mcp@0.0.54)
- Installed Selenium MCP server (selenium-mcp-server-1.2.0)
- Configured Puppeteer MCP server (via npx)
- Updated ~/.claude.json with MCP server configurations
- Created this troubleshooting guide

---

**Document Version:** 1.0
**Last Updated:** 2026-01-04
**Maintained By:** Project Team
