#!/usr/bin/env python3
"""
MCP Server for Conversation Tracking & Multi-Instance Threading
Enables Claude instances to share conversation context
"""

import os
import sys
import asyncio
from typing import List

sys.path.insert(0, os.path.dirname(__file__))

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    Server = None

from conversation_tracker import ConversationTracker


class ConversationTrackerMCPServer:
    """MCP Server for conversation tracking"""

    def __init__(self):
        self.server = Server("conversation-tracker")
        self.tracker = ConversationTracker()
        self._register_handlers()

    def _register_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="create_thread",
                    description="Create a new conversation thread",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "initial_message": {"type": "string"},
                            "claude_instance": {"type": "string", "default": "console"}
                        },
                        "required": ["title"]
                    }
                ),
                types.Tool(
                    name="add_message",
                    description="Add a message to current thread",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "role": {"type": "string", "enum": ["user", "assistant"]},
                            "tools_used": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["content"]
                    }
                ),
                types.Tool(
                    name="list_threads",
                    description="List recent conversation threads",
                    inputSchema={"type": "object", "properties": {}}
                ),
                types.Tool(
                    name="switch_thread",
                    description="Switch to a different thread",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "thread_id": {"type": "string"},
                            "claude_instance": {"type": "string", "default": "console"}
                        },
                        "required": ["thread_id"]
                    }
                ),
                types.Tool(
                    name="get_thread_context",
                    description="Get full context from a thread to share with Claude",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "thread_id": {"type": "string"},
                            "max_messages": {"type": "number", "default": 50}
                        }
                    }
                ),
                types.Tool(
                    name="search_threads",
                    description="Search threads by content",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="export_thread",
                    description="Export thread for sharing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "thread_id": {"type": "string"},
                            "output_path": {"type": "string"}
                        },
                        "required": ["output_path"]
                    }
                ),
                types.Tool(
                    name="import_thread",
                    description="Import thread from another Claude instance",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "input_path": {"type": "string"},
                            "claude_instance": {"type": "string", "default": "console"}
                        },
                        "required": ["input_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> List[types.TextContent]:
            try:
                if name == "create_thread":
                    thread = self.tracker.create_thread(
                        arguments["title"],
                        arguments.get("initial_message"),
                        arguments.get("claude_instance", "console")
                    )
                    return [types.TextContent(
                        type="text",
                        text=f"Created thread '{thread.title}'\nID: {thread.id}\n\n" +
                             f"Use this ID to switch threads or share with other Claude instances."
                    )]

                elif name == "add_message":
                    msg = self.tracker.add_message(
                        arguments["content"],
                        arguments.get("role", "user"),
                        arguments.get("tools_used")
                    )
                    return [types.TextContent(
                        type="text",
                        text=f"Message added to thread (ID: {msg.id})"
                    )]

                elif name == "list_threads":
                    threads = self.tracker.list_threads()
                    text = f"Recent Threads ({len(threads)}):\n\n"
                    for t in threads:
                        active = " [ACTIVE]" if t.id == self.tracker.active_thread_id else ""
                        text += f"• {t.title}{active}\n"
                        text += f"  ID: {t.id}\n"
                        text += f"  Messages: {len(t.messages)}\n"
                        text += f"  Instances: {', '.join(t.claude_instances)}\n\n"
                    return [types.TextContent(type="text", text=text)]

                elif name == "switch_thread":
                    self.tracker.switch_thread(
                        arguments["thread_id"],
                        arguments.get("claude_instance", "console")
                    )
                    summary = self.tracker.get_thread_summary()
                    return [types.TextContent(type="text", text=f"Switched to thread!\n\n{summary}")]

                elif name == "get_thread_context":
                    context = self.tracker.generate_context_for_claude(
                        arguments.get("thread_id"),
                        arguments.get("max_messages", 50)
                    )
                    return [types.TextContent(
                        type="text",
                        text=context or "No thread context available"
                    )]

                elif name == "search_threads":
                    results = self.tracker.search_threads(arguments["query"])
                    text = f"Found {len(results)} thread(s):\n\n"
                    for t in results:
                        text += f"• {t.title}\n  ID: {t.id}\n\n"
                    return [types.TextContent(type="text", text=text)]

                elif name == "export_thread":
                    self.tracker.export_thread(
                        arguments.get("thread_id") or self.tracker.active_thread_id,
                        arguments["output_path"]
                    )
                    return [types.TextContent(
                        type="text",
                        text=f"Thread exported to: {arguments['output_path']}"
                    )]

                elif name == "import_thread":
                    thread = self.tracker.import_thread(
                        arguments["input_path"],
                        arguments.get("claude_instance", "console")
                    )
                    return [types.TextContent(
                        type="text",
                        text=f"Imported thread '{thread.title}' (ID: {thread.id})"
                    )]

            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, InitializationOptions(
                server_name="conversation-tracker",
                server_version="1.0.0",
                capabilities=self.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            ))


if __name__ == "__main__":
    if Server is None:
        print("Error: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
        sys.exit(1)

    asyncio.run(ConversationTrackerMCPServer().run())
