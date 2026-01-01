#!/usr/bin/env python3
"""
MCP Server for Claude Files API Integration
Exposes file upload/management tools via Model Context Protocol
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python-client'))

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Warning: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    Server = None

from claude_files_api import ClaudeFilesAPI


class FileUploadMCPServer:
    """MCP Server providing file upload capabilities"""

    def __init__(self):
        """Initialize the MCP server"""
        self.server = Server("claude-files-api")
        self.files_client = None
        self._register_handlers()

    def _register_handlers(self):
        """Register MCP tool handlers"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="upload_file",
                    description="Upload a file to Claude Files API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to file"},
                            "purpose": {"type": "string", "default": "assistants"}
                        },
                        "required": ["file_path"]
                    }
                ),
                types.Tool(
                    name="list_files",
                    description="List all uploaded files",
                    inputSchema={"type": "object", "properties": {}}
                ),
                types.Tool(
                    name="delete_file",
                    description="Delete a file",
                    inputSchema={
                        "type": "object",
                        "properties": {"file_id": {"type": "string"}},
                        "required": ["file_id"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> List[types.TextContent]:
            """Handle tool execution"""
            if self.files_client is None:
                self.files_client = ClaudeFilesAPI()

            try:
                if name == "upload_file":
                    result = self.files_client.upload_file(arguments.get("file_path"))
                    return [types.TextContent(type="text", text=f"Uploaded: {result.get('id')}")]
                elif name == "list_files":
                    result = self.files_client.list_files()
                    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
                elif name == "delete_file":
                    self.files_client.delete_file(arguments.get("file_id"))
                    return [types.TextContent(type="text", text="Deleted successfully")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, InitializationOptions(
                server_name="claude-files-api", server_version="1.0.0",
                capabilities=self.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            ))


if __name__ == "__main__":
    asyncio.run(FileUploadMCPServer().run())
