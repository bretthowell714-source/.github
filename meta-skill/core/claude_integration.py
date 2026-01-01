#!/usr/bin/env python3
"""
Claude Integration Layer - Connects Meta-Skill Engine with Claude conversations
Automatically learns from Claude interactions and embeds new capabilities
"""

import os
import json
import datetime
from typing import List, Dict, Any, Optional
from meta_skill_engine import MetaSkillEngine, Skill, ConversationContext


class ClaudeMetaSkillIntegration:
    """
    Integration layer that monitors Claude conversations and auto-learns
    """

    def __init__(self, engine: Optional[MetaSkillEngine] = None):
        """Initialize the Claude integration"""
        self.engine = engine or MetaSkillEngine()
        self.current_session = {
            'start_time': datetime.datetime.now().isoformat(),
            'interactions': [],
            'tools_discovered': set(),
            'skills_used': set()
        }

    def process_user_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and get recommendations

        Args:
            query: User's question or request

        Returns:
            Dictionary with recommendations and context
        """
        # Get skill recommendations
        recommended_skills = self.engine.get_recommendations(query)

        # Extract patterns from query
        patterns = self._extract_patterns(query)

        return {
            'query': query,
            'recommended_skills': recommended_skills,
            'detected_patterns': patterns,
            'timestamp': datetime.datetime.now().isoformat()
        }

    def record_tool_usage(self, tool_name: str, context: str, success: bool = True):
        """
        Record tool usage in the current session

        Args:
            tool_name: Name of the tool used
            context: Context in which tool was used
            success: Whether the tool usage was successful
        """
        self.current_session['tools_discovered'].add(tool_name)
        self.current_session['interactions'].append({
            'type': 'tool_usage',
            'tool': tool_name,
            'context': context,
            'success': success,
            'timestamp': datetime.datetime.now().isoformat()
        })

    def record_web_research(self, query: str, sources: List[str], findings: List[str]):
        """
        Record web research and extract learnings

        Args:
            query: Research query
            sources: List of URLs/sources
            findings: Key findings from research
        """
        # Record the interaction
        self.current_session['interactions'].append({
            'type': 'web_research',
            'query': query,
            'sources': sources,
            'findings': findings,
            'timestamp': datetime.datetime.now().isoformat()
        })

        # Try to discover new skills from findings
        for finding in findings:
            skill = self.engine.discover_new_skill_from_web(query, finding)
            if skill:
                self.current_session['skills_used'].add(skill.name)

    def finalize_interaction(self, user_query: str, outcome: str = 'success',
                           learned_items: Optional[List[str]] = None):
        """
        Finalize and record a complete interaction

        Args:
            user_query: The original user query
            outcome: 'success' or 'failure'
            learned_items: Optional list of knowledge items learned
        """
        context = ConversationContext(
            timestamp=datetime.datetime.now().isoformat(),
            user_query=user_query,
            tools_used=list(self.current_session['tools_discovered']),
            outcome=outcome,
            learned_patterns=self._extract_patterns(user_query),
            knowledge_gained=learned_items or []
        )

        self.engine.record_interaction(context)

        # Reset session for next interaction
        self.current_session = {
            'start_time': datetime.datetime.now().isoformat(),
            'interactions': [],
            'tools_discovered': set(),
            'skills_used': set()
        }

    def embed_custom_skill(self, name: str, description: str,
                          category: str, patterns: List[str],
                          tools: List[str], examples: Optional[List[Dict]] = None):
        """
        Manually embed a custom skill

        Args:
            name: Skill name
            description: Skill description
            category: Skill category
            patterns: List of trigger patterns
            tools: List of tools used by this skill
            examples: Optional examples
        """
        skill = Skill(
            name=name,
            description=description,
            category=category,
            patterns=patterns,
            tools_used=tools,
            examples=examples or []
        )

        self.engine.embed_skill(skill)
        return skill

    def learn_from_file(self, file_path: str):
        """
        Learn skills and patterns from a file (e.g., documentation, code)

        Args:
            file_path: Path to file to learn from
        """
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract potential skills (simple pattern matching)
        # In a real implementation, this would use NLP/AI

        if 'class' in content or 'def' in content:
            # Code file - extract function/class patterns
            self._learn_from_code(content)
        elif 'http' in content or 'api' in content.lower():
            # API documentation
            self._learn_from_api_docs(content)

    def _extract_patterns(self, text: str) -> List[str]:
        """Extract meaningful patterns from text"""
        patterns = []
        text_lower = text.lower()

        # Common action patterns
        actions = ['create', 'build', 'implement', 'upload', 'download',
                  'search', 'find', 'analyze', 'generate', 'deploy',
                  'configure', 'setup', 'install', 'integrate']

        for action in actions:
            if action in text_lower:
                patterns.append(action)

        # Technology patterns
        techs = ['python', 'javascript', 'docker', 'api', 'github',
                'mcp', 'vscode', 'android', 'web', 'mobile']

        for tech in techs:
            if tech in text_lower:
                patterns.append(tech)

        return patterns

    def _learn_from_code(self, code: str):
        """Learn patterns from code"""
        # Extract imports to discover libraries
        import_patterns = ['import ', 'from ', 'require(']

        for line in code.split('\n'):
            for pattern in import_patterns:
                if pattern in line:
                    self.current_session['tools_discovered'].add(
                        line.strip().split()[1].split('.')[0]
                    )

    def _learn_from_api_docs(self, docs: str):
        """Learn API patterns from documentation"""
        # Simple extraction - would be more sophisticated in production
        if 'POST' in docs or 'GET' in docs:
            self.current_session['tools_discovered'].add('http_client')
        if 'authentication' in docs.lower():
            self.current_session['tools_discovered'].add('auth')

    def get_session_summary(self) -> str:
        """Get a summary of the current session"""
        summary = []
        summary.append("Current Session Summary:")
        summary.append(f"  Start Time: {self.current_session['start_time']}")
        summary.append(f"  Interactions: {len(self.current_session['interactions'])}")
        summary.append(f"  Tools Discovered: {len(self.current_session['tools_discovered'])}")
        summary.append(f"  Skills Used: {len(self.current_session['skills_used'])}")

        if self.current_session['tools_discovered']:
            summary.append(f"\n  Tools: {', '.join(self.current_session['tools_discovered'])}")

        if self.current_session['skills_used']:
            summary.append(f"  Skills: {', '.join(self.current_session['skills_used'])}")

        return "\n".join(summary)

    def auto_update_from_conversation(self, conversation_log: List[Dict[str, str]]):
        """
        Automatically update skills from a conversation log

        Args:
            conversation_log: List of conversation turns with 'role' and 'content'
        """
        for turn in conversation_log:
            if turn['role'] == 'user':
                # Analyze user queries
                patterns = self._extract_patterns(turn['content'])

            elif turn['role'] == 'assistant':
                # Analyze assistant responses for tool usage
                content = turn['content']

                # Detect tool usage (simple pattern matching)
                if 'tool_use' in content or 'function_call' in content:
                    # Extract tool names from content
                    # This would be more sophisticated in production
                    pass

        # Finalize learning
        self.finalize_interaction(
            user_query="Auto-learned from conversation",
            outcome='success',
            learned_items=[f"Pattern: {p}" for p in patterns]
        )


# Example usage
def example_workflow():
    """Example workflow demonstrating the integration"""
    # Initialize
    integration = ClaudeMetaSkillIntegration()

    # Process user query
    result = integration.process_user_query(
        "I want to upload files to Anthropic API and create a Docker container"
    )
    print(f"Recommendations: {result['recommended_skills']}")

    # Record tool usage
    integration.record_tool_usage('anthropic_api', 'file upload', success=True)
    integration.record_tool_usage('docker', 'container creation', success=True)

    # Record web research
    integration.record_web_research(
        query="Docker best practices",
        sources=["https://docs.docker.com"],
        findings=["Use multi-stage builds", "Minimize layer count"]
    )

    # Embed custom skill
    integration.embed_custom_skill(
        name="docker_deployment",
        description="Deploy applications using Docker",
        category="devops",
        patterns=["docker", "deploy", "container"],
        tools=["docker", "docker-compose"]
    )

    # Finalize interaction
    integration.finalize_interaction(
        user_query="Upload files and create Docker container",
        outcome='success',
        learned_items=[
            "Anthropic API supports file uploads",
            "Docker multi-stage builds reduce image size"
        ]
    )

    # Get session summary
    print("\n" + integration.get_session_summary())

    # Generate report
    print("\n" + integration.engine.generate_skill_report())


if __name__ == "__main__":
    example_workflow()
