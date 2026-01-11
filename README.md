# GitHub Configuration Repository

This repository contains configuration files for GitHub and development tools.

## MCP Server Configuration

This repository includes an MCP (Model Context Protocol) server configuration for Selenium browser automation.

### Selenium MCP Server

The `.mcp.json` file configures the Selenium MCP server, which provides browser automation capabilities through Claude Code.

**Features:**
- Navigate to web pages
- Interact with page elements (click, type, scroll)
- Take screenshots
- Extract page content and data
- Execute JavaScript in the browser
- Handle multiple browser sessions

**Usage:**
When using Claude Code in this repository, the Selenium MCP server will be automatically available. You can request browser automation tasks such as:
- "Navigate to example.com and take a screenshot"
- "Click the login button and fill in the form"
- "Extract all links from the page"

**Requirements:**
- Node.js installed on your system
- The server will be automatically installed via npx when first used

## Files

- `.mcp.json` - MCP server configuration for Selenium
- `SECURITY.md` - Security policy and vulnerability reporting guidelines
