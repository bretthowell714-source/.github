#!/usr/bin/env python3
"""
Comprehensive Test Suite for Meta-Skill Engine
Proves that self-embedding and learning actually works
"""

import os
import sys
import json
import yaml
import tempfile
import shutil
from pathlib import Path
import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from meta_skill_engine import MetaSkillEngine, Skill, ConversationContext
from claude_integration import ClaudeMetaSkillIntegration


class TestMetaSkillEngine:
    """Test suite with visual proof of changes"""

    def __init__(self):
        """Initialize test environment"""
        self.test_dir = tempfile.mkdtemp(prefix='meta_skill_test_')
        self.engine = MetaSkillEngine(config_dir=self.test_dir)
        self.integration = ClaudeMetaSkillIntegration(engine=self.engine)
        self.test_results = []

    def cleanup(self):
        """Clean up test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        print(f"{status} | {test_name}")
        if details:
            print(f"      {details}")

    def print_file_contents(self, file_path: str, label: str):
        """Print file contents for visual verification"""
        print(f"\n{'='*80}")
        print(f"FILE CONTENTS: {label}")
        print(f"Path: {file_path}")
        print(f"{'='*80}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                print(content)
                print(f"{'='*80}\n")
                return content
        else:
            print("FILE DOES NOT EXIST!")
            print(f"{'='*80}\n")
            return None

    def test_01_initialization(self):
        """Test 1: Verify system initializes with default skills"""
        print("\n" + "="*80)
        print("TEST 1: System Initialization")
        print("="*80)

        initial_skills = len(self.engine.skills)
        print(f"Initial skills count: {initial_skills}")

        # Check that default skills were created
        expected_skills = ['file_upload', 'web_research', 'code_generation',
                          'mcp_integration', 'self_embedding']

        all_present = all(skill in self.engine.skills for skill in expected_skills)

        self.log_result(
            "Initialization with default skills",
            all_present and initial_skills >= 5,
            f"Found {initial_skills} skills: {list(self.engine.skills.keys())}"
        )

        # Verify config files were created
        config_files = list(Path(self.test_dir).glob('*.{json,yaml}'))
        self.log_result(
            "Config files created",
            len(config_files) > 0,
            f"Created files: {[f.name for f in config_files]}"
        )

    def test_02_skill_embedding(self):
        """Test 2: Prove that new skills are actually embedded"""
        print("\n" + "="*80)
        print("TEST 2: Skill Embedding (PROOF OF CHANGE)")
        print("="*80)

        # Get initial state
        initial_count = len(self.engine.skills)
        print(f"Skills BEFORE embedding: {initial_count}")
        print(f"Skill names: {list(self.engine.skills.keys())}\n")

        # Create and embed a new skill
        new_skill = Skill(
            name="test_automation",
            description="Automated testing capabilities",
            category="testing",
            patterns=["test", "verify", "validate"],
            tools_used=["pytest", "unittest"]
        )

        print(f"Embedding new skill: '{new_skill.name}'...")
        success = self.engine.embed_skill(new_skill)

        # Get new state
        new_count = len(self.engine.skills)
        print(f"\nSkills AFTER embedding: {new_count}")
        print(f"Skill names: {list(self.engine.skills.keys())}")

        # Verify the change
        count_increased = new_count == initial_count + 1
        skill_exists = "test_automation" in self.engine.skills

        self.log_result(
            "Skill successfully embedded",
            count_increased and skill_exists,
            f"Count increased from {initial_count} to {new_count}"
        )

        # Prove it was saved to disk
        content = self.print_file_contents(
            str(self.engine.skills_file),
            "Skills Registry (YAML)"
        )

        disk_saved = content and "test_automation" in content

        self.log_result(
            "Skill persisted to disk",
            disk_saved,
            "Skill found in skills_registry.yaml"
        )

    def test_03_knowledge_accumulation(self):
        """Test 3: Prove knowledge is accumulated and persisted"""
        print("\n" + "="*80)
        print("TEST 3: Knowledge Accumulation (PROOF OF LEARNING)")
        print("="*80)

        # Get initial state
        initial_facts = len(self.engine.knowledge_base['facts'])
        print(f"Knowledge items BEFORE: {initial_facts}\n")

        # Record multiple interactions with learnings
        learnings = [
            "Anthropic API uses x-api-key header for authentication",
            "Docker multi-stage builds reduce image size",
            "MCP servers enable tool integration",
            "VSCode extensions use TypeScript"
        ]

        for i, learning in enumerate(learnings):
            context = ConversationContext(
                timestamp=datetime.datetime.now().isoformat(),
                user_query=f"Learning session {i+1}",
                tools_used=['research'],
                outcome='success',
                learned_patterns=['research', 'documentation'],
                knowledge_gained=[learning]
            )
            print(f"Recording learning: {learning}")
            self.engine.record_interaction(context)

        # Get new state
        new_facts = len(self.engine.knowledge_base['facts'])
        print(f"\nKnowledge items AFTER: {new_facts}")
        print(f"Items added: {new_facts - initial_facts}")

        self.log_result(
            "Knowledge accumulated",
            new_facts == initial_facts + len(learnings),
            f"Added {len(learnings)} knowledge items"
        )

        # Prove it was saved to disk
        content = self.print_file_contents(
            str(self.engine.knowledge_file),
            "Knowledge Base (JSON)"
        )

        knowledge_saved = content and "Anthropic API" in content

        self.log_result(
            "Knowledge persisted to disk",
            knowledge_saved,
            "Knowledge items found in knowledge_base.json"
        )

    def test_04_tool_usage_tracking(self):
        """Test 4: Prove tool usage is tracked across interactions"""
        print("\n" + "="*80)
        print("TEST 4: Tool Usage Tracking (PROOF OF MONITORING)")
        print("="*80)

        # Get initial state
        print("Tool usage BEFORE:")
        for tool, data in list(self.engine.tool_usage.items())[:3]:
            print(f"  {tool}: {data['count']} uses")

        # Record multiple tool usages
        tools_to_use = [
            ('anthropic_api', 'file upload'),
            ('docker', 'container build'),
            ('anthropic_api', 'chat completion'),
            ('github_api', 'repo creation'),
            ('anthropic_api', 'embeddings')
        ]

        print(f"\nSimulating {len(tools_to_use)} tool usages...")
        for tool, context_desc in tools_to_use:
            self.integration.record_tool_usage(tool, context_desc, success=True)

        # Finalize to save
        self.integration.finalize_interaction(
            "Tool usage test",
            outcome='success'
        )

        print("\nTool usage AFTER:")
        for tool in ['anthropic_api', 'docker', 'github_api']:
            count = self.engine.tool_usage.get(tool, {}).get('count', 0)
            print(f"  {tool}: {count} uses")

        # Verify tracking
        anthropic_count = self.engine.tool_usage['anthropic_api']['count']

        self.log_result(
            "Tool usage tracked",
            anthropic_count >= 3,
            f"anthropic_api used {anthropic_count} times"
        )

        # Prove it was saved
        content = self.print_file_contents(
            str(self.engine.tools_file),
            "Tool Usage Stats (JSON)"
        )

        tools_saved = content and "anthropic_api" in content

        self.log_result(
            "Tool usage persisted to disk",
            tools_saved,
            "Tool statistics found in tool_usage.json"
        )

    def test_05_pattern_learning(self):
        """Test 5: Prove patterns are learned and stored"""
        print("\n" + "="*80)
        print("TEST 5: Pattern Learning (PROOF OF ADAPTATION)")
        print("="*80)

        # Get initial state
        initial_patterns = dict(self.engine.learned_patterns)
        print(f"Pattern categories BEFORE: {list(initial_patterns.keys())}")

        # Record interactions with different patterns
        test_cases = [
            ("upload files to API", ["upload", "api", "files"]),
            ("create Docker container", ["create", "docker", "container"]),
            ("search GitHub repositories", ["search", "github"])
        ]

        for query, patterns in test_cases:
            context = ConversationContext(
                timestamp=datetime.datetime.now().isoformat(),
                user_query=query,
                tools_used=['pattern_detector'],
                outcome='success',
                learned_patterns=patterns,
                knowledge_gained=[]
            )
            print(f"Learning patterns from: '{query}'")
            print(f"  Patterns: {patterns}")
            self.engine.record_interaction(context)

        # Get new state
        new_patterns = dict(self.engine.learned_patterns)
        print(f"\nPattern categories AFTER: {list(new_patterns.keys())}")
        print(f"Success patterns: {new_patterns.get('success', [])}")

        patterns_learned = len(new_patterns.get('success', [])) > len(initial_patterns.get('success', []))

        self.log_result(
            "Patterns learned from interactions",
            patterns_learned,
            f"Learned {len(new_patterns.get('success', []))} patterns"
        )

        # Prove it was saved
        content = self.print_file_contents(
            str(self.engine.patterns_file),
            "Learned Patterns (JSON)"
        )

        patterns_saved = content and "upload" in content

        self.log_result(
            "Patterns persisted to disk",
            patterns_saved,
            "Patterns found in learned_patterns.json"
        )

    def test_06_skill_auto_update(self):
        """Test 6: Prove skills auto-update based on usage"""
        print("\n" + "="*80)
        print("TEST 6: Skill Auto-Update (PROOF OF EVOLUTION)")
        print("="*80)

        # Get initial state of a skill
        skill_name = "file_upload"
        initial_usage = self.engine.skills[skill_name].usage_count
        initial_examples = len(self.engine.skills[skill_name].examples)

        print(f"Skill '{skill_name}' BEFORE:")
        print(f"  Usage count: {initial_usage}")
        print(f"  Examples: {initial_examples}")
        print(f"  Tools: {self.engine.skills[skill_name].tools_used}")

        # Simulate interactions that trigger this skill
        for i in range(3):
            context = ConversationContext(
                timestamp=datetime.datetime.now().isoformat(),
                user_query=f"upload file number {i+1}",
                tools_used=['requests', 'new_tool_discovered'],
                outcome='success',
                learned_patterns=['upload', 'file'],
                knowledge_gained=[]
            )
            self.engine.record_interaction(context)

        # Get new state
        new_usage = self.engine.skills[skill_name].usage_count
        new_examples = len(self.engine.skills[skill_name].examples)
        new_tools = self.engine.skills[skill_name].tools_used

        print(f"\nSkill '{skill_name}' AFTER:")
        print(f"  Usage count: {new_usage}")
        print(f"  Examples: {new_examples}")
        print(f"  Tools: {new_tools}")

        # Verify auto-update
        usage_increased = new_usage > initial_usage
        new_tool_added = 'new_tool_discovered' in new_tools

        self.log_result(
            "Skill auto-updated from usage",
            usage_increased and new_tool_added,
            f"Usage: {initial_usage} → {new_usage}, New tool added"
        )

        # Show the updated config
        self.print_file_contents(
            str(self.engine.skills_file),
            "Updated Skills Registry"
        )

    def test_07_conversation_history(self):
        """Test 7: Prove conversation history is recorded"""
        print("\n" + "="*80)
        print("TEST 7: Conversation History (PROOF OF MEMORY)")
        print("="*80)

        # Get initial state
        initial_count = len(self.engine.conversation_history)
        print(f"Conversation entries BEFORE: {initial_count}")

        # Record several conversations
        conversations = [
            "How do I upload files?",
            "Create a Docker container",
            "Search for Python libraries",
            "Deploy to production"
        ]

        for query in conversations:
            context = ConversationContext(
                timestamp=datetime.datetime.now().isoformat(),
                user_query=query,
                tools_used=['various'],
                outcome='success',
                learned_patterns=[],
                knowledge_gained=[]
            )
            self.engine.record_interaction(context)
            print(f"Recorded: {query}")

        # Get new state
        new_count = len(self.engine.conversation_history)
        print(f"\nConversation entries AFTER: {new_count}")
        print(f"New entries: {new_count - initial_count}")

        self.log_result(
            "Conversation history recorded",
            new_count == initial_count + len(conversations),
            f"Recorded {len(conversations)} conversations"
        )

        # Prove it was saved
        content = self.print_file_contents(
            str(self.engine.history_file),
            "Conversation History (JSON)"
        )

        history_saved = content and "upload files" in content

        self.log_result(
            "History persisted to disk",
            history_saved,
            "Conversations found in conversation_history.json"
        )

    def test_08_export_import(self):
        """Test 8: Prove full system export/import works"""
        print("\n" + "="*80)
        print("TEST 8: Export/Import (PROOF OF PORTABILITY)")
        print("="*80)

        # Export current state
        export_path = os.path.join(self.test_dir, 'exported_config.yaml')
        print(f"Exporting system to: {export_path}")
        self.engine.export_system_config(export_path)

        # Verify export file exists and has content
        export_content = self.print_file_contents(
            export_path,
            "Exported System Configuration"
        )

        export_success = (
            os.path.exists(export_path) and
            export_content and
            'skills' in export_content and
            'knowledge_base' in export_content
        )

        self.log_result(
            "System configuration exported",
            export_success,
            f"Exported to {os.path.basename(export_path)}"
        )

        # Create a new engine and import
        new_test_dir = tempfile.mkdtemp(prefix='meta_skill_import_')
        new_engine = MetaSkillEngine(config_dir=new_test_dir)

        initial_skills = len(new_engine.skills)
        print(f"\nNew engine skills BEFORE import: {initial_skills}")

        print(f"Importing from: {export_path}")
        new_engine.import_system_config(export_path)

        imported_skills = len(new_engine.skills)
        print(f"New engine skills AFTER import: {imported_skills}")

        import_success = imported_skills >= len(self.engine.skills)

        self.log_result(
            "System configuration imported",
            import_success,
            f"Imported {imported_skills} skills"
        )

        # Cleanup
        shutil.rmtree(new_test_dir)

    def test_09_skill_recommendations(self):
        """Test 9: Prove recommendation engine works"""
        print("\n" + "="*80)
        print("TEST 9: Skill Recommendations (PROOF OF INTELLIGENCE)")
        print("="*80)

        test_queries = [
            "I need to upload a PDF file",
            "How do I create a Docker container?",
            "Search the web for information",
            "Write Python code for API integration"
        ]

        for query in test_queries:
            recommendations = self.engine.get_recommendations(query)
            print(f"\nQuery: '{query}'")
            print(f"Recommendations: {recommendations}")

            has_recommendations = len(recommendations) > 0

            self.log_result(
                f"Recommendations for: {query[:40]}...",
                has_recommendations,
                f"Suggested: {', '.join(recommendations[:3])}"
            )

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("\n" + "█"*80)
        print("META-SKILL ENGINE - COMPREHENSIVE TEST SUITE")
        print("Proving that self-embedding and learning actually works")
        print("█"*80)

        try:
            # Run all tests
            self.test_01_initialization()
            self.test_02_skill_embedding()
            self.test_03_knowledge_accumulation()
            self.test_04_tool_usage_tracking()
            self.test_05_pattern_learning()
            self.test_06_skill_auto_update()
            self.test_07_conversation_history()
            self.test_08_export_import()
            self.test_09_skill_recommendations()

            # Generate final report
            self.generate_final_report()

        finally:
            self.cleanup()

    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "█"*80)
        print("FINAL TEST REPORT")
        print("█"*80)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests

        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✓")
        print(f"Failed: {failed_tests} ✗")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        if failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  ✗ {result['test']}")
                    if result['details']:
                        print(f"    {result['details']}")

        print("\n" + "█"*80)
        if failed_tests == 0:
            print("ALL TESTS PASSED! ✓")
            print("Self-embedding system is PROVEN to work!")
        else:
            print(f"SOME TESTS FAILED ({failed_tests}/{total_tests})")
        print("█"*80)

        # Show final system state
        print("\n" + self.engine.generate_skill_report())


if __name__ == "__main__":
    print("Starting comprehensive test suite...")
    print("This will prove that the meta-skill engine actually works!\n")

    tester = TestMetaSkillEngine()
    tester.run_all_tests()
