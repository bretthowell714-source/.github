#!/usr/bin/env python3
"""
MCP Server for Meta-Skill Engine
Exposes self-embedding skill system via MCP
"""

import os
import sys
import json
import asyncio
from typing import List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'meta-skill', 'core'))

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    Server = None

from meta_skill_engine import MetaSkillEngine, Skill, ConversationContext
from claude_integration import ClaudeMetaSkillIntegration
import datetime


class MetaSkillMCPServer:
    """MCP Server for meta-skill capabilities"""

    def __init__(self):
        self.server = Server("meta-skill-engine")
        self.engine = MetaSkillEngine()
        self.integration = ClaudeMetaSkillIntegration(self.engine)
        self._register_handlers()

    def _register_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="embed_skill",
                    description="Embed a new skill into the system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "category": {"type": "string"},
                            "patterns": {"type": "array", "items": {"type": "string"}},
                            "tools": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["name", "description", "category"]
                    }
                ),
                types.Tool(
                    name="get_recommendations",
                    description="Get skill recommendations for a query",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="record_learning",
                    description="Record learned knowledge",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "tools_used": {"type": "array", "items": {"type": "string"}},
                            "knowledge": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="generate_report",
                    description="Generate skill system report",
                    inputSchema={"type": "object", "properties": {}}
                ),
                types.Tool(
                    name="export_config",
                    description="Export system configuration",
                    inputSchema={
                        "type": "object",
                        "properties": {"output_path": {"type": "string"}},
                        "required": ["output_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> List[types.TextContent]:
            try:
                if name == "embed_skill":
                    skill = Skill(
                        name=arguments["name"],
                        description=arguments["description"],
                        category=arguments["category"],
                        patterns=arguments.get("patterns", []),
                        tools_used=arguments.get("tools", [])
                    )
                    self.engine.embed_skill(skill)
                    return [types.TextContent(type="text", text=f"Skill '{skill.name}' embedded!")]

                elif name == "get_recommendations":
                    recs = self.engine.get_recommendations(arguments["query"])
                    return [types.TextContent(type="text", text=f"Recommended: {', '.join(recs)}")]

                elif name == "record_learning":
                    context = ConversationContext(
                        timestamp=datetime.datetime.now().isoformat(),
                        user_query=arguments["query"],
                        tools_used=arguments.get("tools_used", []),
                        outcome="success",
                        learned_patterns=[],
                        knowledge_gained=arguments.get("knowledge", [])
                    )
                    self.engine.record_interaction(context)
                    return [types.TextContent(type="text", text="Learning recorded!")]

                elif name == "generate_report":
                    report = self.engine.generate_skill_report()
                    return [types.TextContent(type="text", text=report)]

                elif name == "export_config":
                    self.engine.export_system_config(arguments["output_path"])
                    return [types.TextContent(type="text", text=f"Exported to {arguments['output_path']}")]

            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, InitializationOptions(
                server_name="meta-skill-engine", server_version="1.0.0",
                capabilities=self.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            ))


if __name__ == "__main__":
    asyncio.run(MetaSkillMCPServer().run())
