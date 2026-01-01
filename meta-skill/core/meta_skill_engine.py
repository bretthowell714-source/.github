#!/usr/bin/env python3
"""
Meta-Skill Engine - Self-Embedding Skill System
A self-modifying AI skill framework that learns from interactions and auto-updates
"""

import os
import json
import yaml
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class Skill:
    """Represents a single skill with metadata"""
    name: str
    description: str
    category: str
    usage_count: int = 0
    success_rate: float = 1.0
    last_used: Optional[str] = None
    patterns: List[str] = None
    tools_used: List[str] = None
    examples: List[Dict[str, str]] = None

    def __post_init__(self):
        if self.patterns is None:
            self.patterns = []
        if self.tools_used is None:
            self.tools_used = []
        if self.examples is None:
            self.examples = []


@dataclass
class ConversationContext:
    """Captures conversation context for learning"""
    timestamp: str
    user_query: str
    tools_used: List[str]
    outcome: str
    learned_patterns: List[str]
    knowledge_gained: List[str]


class MetaSkillEngine:
    """
    Self-embedding skill engine that learns and evolves
    """

    def __init__(self, config_dir: str = None):
        """Initialize the meta-skill engine"""
        self.config_dir = Path(config_dir or os.path.join(os.path.dirname(__file__), '..', 'config'))
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.skills_file = self.config_dir / 'skills_registry.yaml'
        self.knowledge_file = self.config_dir / 'knowledge_base.json'
        self.patterns_file = self.config_dir / 'learned_patterns.json'
        self.tools_file = self.config_dir / 'tool_usage.json'
        self.history_file = self.config_dir / 'conversation_history.json'

        # Load existing data
        self.skills = self._load_skills()
        self.knowledge_base = self._load_knowledge()
        self.learned_patterns = self._load_patterns()
        self.tool_usage = self._load_tool_usage()
        self.conversation_history = self._load_history()

    def _load_skills(self) -> Dict[str, Skill]:
        """Load skills from registry"""
        if self.skills_file.exists():
            with open(self.skills_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                return {
                    name: Skill(**skill_data)
                    for name, skill_data in data.items()
                }
        return self._initialize_default_skills()

    def _initialize_default_skills(self) -> Dict[str, Skill]:
        """Initialize with default skills"""
        return {
            'file_upload': Skill(
                name='file_upload',
                description='Upload files to Anthropic Files API',
                category='api_integration',
                patterns=['upload', 'file', 'api'],
                tools_used=['requests', 'anthropic_api']
            ),
            'web_research': Skill(
                name='web_research',
                description='Research and gather information from the internet',
                category='research',
                patterns=['search', 'research', 'find information'],
                tools_used=['web_search', 'web_fetch']
            ),
            'code_generation': Skill(
                name='code_generation',
                description='Generate code across multiple languages',
                category='development',
                patterns=['create', 'build', 'implement', 'write code'],
                tools_used=['write', 'edit']
            ),
            'mcp_integration': Skill(
                name='mcp_integration',
                description='Integrate with Model Context Protocol servers',
                category='integration',
                patterns=['mcp', 'tool', 'server'],
                tools_used=['mcp_client']
            ),
            'self_embedding': Skill(
                name='self_embedding',
                description='Embed new skills and knowledge into the system',
                category='meta',
                patterns=['learn', 'embed', 'update', 'self-improve'],
                tools_used=['yaml', 'json', 'file_operations']
            )
        }

    def _load_knowledge(self) -> Dict[str, Any]:
        """Load knowledge base"""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        return {
            'facts': {},
            'procedures': {},
            'apis': {},
            'best_practices': {},
            'errors_learned': {}
        }

    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load learned patterns"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return defaultdict(list)

    def _load_tool_usage(self) -> Dict[str, Dict]:
        """Load tool usage statistics"""
        if self.tools_file.exists():
            with open(self.tools_file, 'r') as f:
                return json.load(f)
        return defaultdict(lambda: {'count': 0, 'contexts': []})

    def _load_history(self) -> List[Dict]:
        """Load conversation history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_all(self):
        """Persist all data to disk"""
        # Save skills
        with open(self.skills_file, 'w') as f:
            yaml.dump(
                {name: asdict(skill) for name, skill in self.skills.items()},
                f,
                default_flow_style=False
            )

        # Save knowledge base
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)

        # Save patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(dict(self.learned_patterns), f, indent=2)

        # Save tool usage
        with open(self.tools_file, 'w') as f:
            json.dump(dict(self.tool_usage), f, indent=2)

        # Save conversation history (keep last 1000)
        with open(self.history_file, 'w') as f:
            json.dump(self.conversation_history[-1000:], f, indent=2)

    def embed_skill(self, skill: Skill) -> bool:
        """
        Embed a new skill into the system

        Args:
            skill: Skill object to embed

        Returns:
            True if successfully embedded
        """
        self.skills[skill.name] = skill
        self.save_all()
        return True

    def record_interaction(self, context: ConversationContext):
        """
        Record a conversation interaction for learning

        Args:
            context: ConversationContext with interaction details
        """
        # Add to history
        self.conversation_history.append(asdict(context))

        # Update tool usage
        for tool in context.tools_used:
            self.tool_usage[tool]['count'] += 1
            self.tool_usage[tool]['contexts'].append({
                'query': context.user_query[:100],
                'timestamp': context.timestamp,
                'outcome': context.outcome
            })

        # Learn patterns
        for pattern in context.learned_patterns:
            if pattern not in self.learned_patterns[context.outcome]:
                self.learned_patterns[context.outcome].append(pattern)

        # Store knowledge
        for knowledge in context.knowledge_gained:
            knowledge_hash = hashlib.md5(knowledge.encode()).hexdigest()
            self.knowledge_base['facts'][knowledge_hash] = {
                'content': knowledge,
                'learned_at': context.timestamp,
                'source': context.user_query[:100]
            }

        # Auto-update skills based on usage
        self._update_skill_from_interaction(context)

        # Persist changes
        self.save_all()

    def _update_skill_from_interaction(self, context: ConversationContext):
        """Update skills based on interaction patterns"""
        # Detect which skills were likely used
        for skill_name, skill in self.skills.items():
            # Check if any patterns match
            query_lower = context.user_query.lower()
            if any(pattern.lower() in query_lower for pattern in skill.patterns):
                skill.usage_count += 1
                skill.last_used = context.timestamp

                # Add new tools if discovered
                for tool in context.tools_used:
                    if tool not in skill.tools_used:
                        skill.tools_used.append(tool)

                # Add example if successful
                if context.outcome == 'success':
                    skill.examples.append({
                        'query': context.user_query[:200],
                        'tools': context.tools_used,
                        'timestamp': context.timestamp
                    })
                    # Keep only last 10 examples
                    skill.examples = skill.examples[-10:]

    def discover_new_skill_from_web(self, topic: str, web_content: str) -> Optional[Skill]:
        """
        Analyze web content to discover and embed new skills

        Args:
            topic: Topic being researched
            web_content: Content from web research

        Returns:
            New skill if discovered, None otherwise
        """
        # This would use AI/NLP to analyze content
        # For now, simple pattern matching

        patterns = []
        tools = []

        # Extract API patterns
        if 'api' in web_content.lower():
            patterns.append('api')
            tools.append('api_client')

        if 'github' in web_content.lower():
            patterns.append('github')
            tools.append('github_api')

        # Create skill if patterns found
        if patterns:
            skill = Skill(
                name=f"{topic.lower().replace(' ', '_')}_skill",
                description=f"Auto-discovered skill for {topic}",
                category='auto_discovered',
                patterns=patterns,
                tools_used=tools
            )
            self.embed_skill(skill)
            return skill

        return None

    def get_recommendations(self, query: str) -> List[str]:
        """
        Get skill recommendations based on query

        Args:
            query: User query

        Returns:
            List of recommended skill names
        """
        recommendations = []
        query_lower = query.lower()

        for skill_name, skill in self.skills.items():
            score = 0

            # Check pattern matches
            for pattern in skill.patterns:
                if pattern.lower() in query_lower:
                    score += 10

            # Boost by usage count and success rate
            score += skill.usage_count * skill.success_rate

            if score > 0:
                recommendations.append((skill_name, score))

        # Sort by score
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return [name for name, score in recommendations[:5]]

    def export_system_config(self, output_path: str):
        """
        Export entire system configuration for portability

        Args:
            output_path: Path to export configuration
        """
        config = {
            'version': '1.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'skills': {name: asdict(skill) for name, skill in self.skills.items()},
            'knowledge_base': self.knowledge_base,
            'learned_patterns': dict(self.learned_patterns),
            'tool_usage': dict(self.tool_usage),
            'stats': {
                'total_skills': len(self.skills),
                'total_interactions': len(self.conversation_history),
                'total_knowledge_items': len(self.knowledge_base['facts'])
            }
        }

        with open(output_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        print(f"System configuration exported to: {output_path}")

    def import_system_config(self, input_path: str):
        """
        Import system configuration

        Args:
            input_path: Path to configuration file
        """
        with open(input_path, 'r') as f:
            config = yaml.safe_load(f)

        # Import skills
        for name, skill_data in config.get('skills', {}).items():
            self.skills[name] = Skill(**skill_data)

        # Import knowledge
        self.knowledge_base.update(config.get('knowledge_base', {}))

        # Import patterns
        for key, values in config.get('learned_patterns', {}).items():
            self.learned_patterns[key].extend(values)

        # Import tool usage
        self.tool_usage.update(config.get('tool_usage', {}))

        self.save_all()
        print(f"System configuration imported from: {input_path}")

    def generate_skill_report(self) -> str:
        """Generate a report of all skills and capabilities"""
        report = []
        report.append("=" * 80)
        report.append("META-SKILL SYSTEM REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Skills: {len(self.skills)}")
        report.append(f"Total Interactions: {len(self.conversation_history)}")
        report.append(f"Total Knowledge Items: {len(self.knowledge_base['facts'])}\n")

        report.append("\nSKILLS BY CATEGORY:")
        report.append("-" * 80)

        by_category = defaultdict(list)
        for skill in self.skills.values():
            by_category[skill.category].append(skill)

        for category, skills in sorted(by_category.items()):
            report.append(f"\n{category.upper()}:")
            for skill in sorted(skills, key=lambda s: s.usage_count, reverse=True):
                report.append(f"  • {skill.name}")
                report.append(f"    - {skill.description}")
                report.append(f"    - Usage: {skill.usage_count} times")
                report.append(f"    - Success Rate: {skill.success_rate:.2%}")
                report.append(f"    - Tools: {', '.join(skill.tools_used)}")

        report.append("\n" + "=" * 80)
        report.append("TOP TOOLS:")
        report.append("-" * 80)

        top_tools = sorted(
            self.tool_usage.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:10]

        for tool, data in top_tools:
            report.append(f"  • {tool}: {data['count']} uses")

        return "\n".join(report)


def main():
    """CLI interface for meta-skill engine"""
    import argparse

    parser = argparse.ArgumentParser(description="Meta-Skill Engine")
    parser.add_argument('command', choices=['init', 'add-skill', 'record', 'report', 'export', 'import'],
                       help='Command to execute')
    parser.add_argument('--name', help='Skill name')
    parser.add_argument('--description', help='Skill description')
    parser.add_argument('--category', help='Skill category')
    parser.add_argument('--patterns', nargs='+', help='Skill patterns')
    parser.add_argument('--file', help='File path for import/export')

    args = parser.parse_args()

    engine = MetaSkillEngine()

    if args.command == 'init':
        engine.save_all()
        print("Meta-skill system initialized!")

    elif args.command == 'add-skill':
        skill = Skill(
            name=args.name,
            description=args.description,
            category=args.category or 'custom',
            patterns=args.patterns or []
        )
        engine.embed_skill(skill)
        print(f"Skill '{args.name}' embedded successfully!")

    elif args.command == 'report':
        print(engine.generate_skill_report())

    elif args.command == 'export':
        output = args.file or 'meta_skill_config.yaml'
        engine.export_system_config(output)

    elif args.command == 'import':
        if not args.file:
            print("Error: --file required for import")
            return
        engine.import_system_config(args.file)


if __name__ == "__main__":
    main()
