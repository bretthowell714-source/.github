#!/usr/bin/env python3
"""
Claude Conversation Tracker & Multi-Instance Threading System
Enables conversation tracking and thread sharing across Claude instances
"""

import os
import json
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Message:
    """Single message in a conversation"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    tools_used: List[str] = None
    attachments: List[str] = None

    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
        if self.attachments is None:
            self.attachments = []


@dataclass
class Thread:
    """Conversation thread that can be shared across Claude instances"""
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[Message]
    metadata: Dict[str, Any]
    claude_instances: List[str]  # Track which Claude instances accessed this

    def __post_init__(self):
        if not isinstance(self.messages[0], Message):
            self.messages = [Message(**msg) if isinstance(msg, dict) else msg
                           for msg in self.messages]


class ConversationTracker:
    """
    Track conversations and enable threading across Claude instances
    """

    def __init__(self, storage_dir: str = None):
        """Initialize tracker"""
        self.storage_dir = Path(storage_dir or os.path.expanduser("~/.claude_threads"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.threads_file = self.storage_dir / "threads.json"
        self.active_thread_file = self.storage_dir / "active_thread.json"

        self.threads: Dict[str, Thread] = self._load_threads()
        self.active_thread_id: Optional[str] = self._load_active_thread()

    def _load_threads(self) -> Dict[str, Thread]:
        """Load all threads from disk"""
        if self.threads_file.exists():
            with open(self.threads_file, 'r') as f:
                data = json.load(f)
                return {
                    thread_id: Thread(**thread_data)
                    for thread_id, thread_data in data.items()
                }
        return {}

    def _load_active_thread(self) -> Optional[str]:
        """Load active thread ID"""
        if self.active_thread_file.exists():
            with open(self.active_thread_file, 'r') as f:
                return json.load(f).get('thread_id')
        return None

    def _save_threads(self):
        """Save all threads to disk"""
        with open(self.threads_file, 'w') as f:
            json.dump(
                {tid: asdict(thread) for tid, thread in self.threads.items()},
                f,
                indent=2
            )

    def _save_active_thread(self):
        """Save active thread ID"""
        with open(self.active_thread_file, 'w') as f:
            json.dump({'thread_id': self.active_thread_id}, f)

    def create_thread(self, title: str, initial_message: Optional[str] = None,
                     claude_instance: str = "console") -> Thread:
        """
        Create a new conversation thread

        Args:
            title: Thread title
            initial_message: Optional first message
            claude_instance: Which Claude instance created this (console, desktop, vscode, etc.)

        Returns:
            Created thread
        """
        thread_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()

        messages = []
        if initial_message:
            messages.append(Message(
                id=str(uuid.uuid4()),
                role="user",
                content=initial_message,
                timestamp=now
            ))

        thread = Thread(
            id=thread_id,
            title=title,
            created_at=now,
            updated_at=now,
            messages=messages,
            metadata={},
            claude_instances=[claude_instance]
        )

        self.threads[thread_id] = thread
        self.active_thread_id = thread_id
        self._save_threads()
        self._save_active_thread()

        return thread

    def add_message(self, content: str, role: str = "user",
                   tools_used: Optional[List[str]] = None,
                   attachments: Optional[List[str]] = None,
                   thread_id: Optional[str] = None) -> Message:
        """
        Add a message to the active or specified thread

        Args:
            content: Message content
            role: 'user' or 'assistant'
            tools_used: List of tools used
            attachments: List of file paths
            thread_id: Optional thread ID (uses active if not specified)

        Returns:
            Created message
        """
        tid = thread_id or self.active_thread_id

        if not tid or tid not in self.threads:
            raise ValueError("No active thread. Create one first.")

        message = Message(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.datetime.now().isoformat(),
            tools_used=tools_used or [],
            attachments=attachments or []
        )

        self.threads[tid].messages.append(message)
        self.threads[tid].updated_at = message.timestamp
        self._save_threads()

        return message

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a specific thread"""
        return self.threads.get(thread_id)

    def get_active_thread(self) -> Optional[Thread]:
        """Get the currently active thread"""
        if self.active_thread_id:
            return self.threads.get(self.active_thread_id)
        return None

    def switch_thread(self, thread_id: str, claude_instance: str = "console"):
        """
        Switch to a different thread

        Args:
            thread_id: Thread to switch to
            claude_instance: Which Claude instance is switching
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread {thread_id} not found")

        self.active_thread_id = thread_id

        # Track which Claude instance accessed this thread
        if claude_instance not in self.threads[thread_id].claude_instances:
            self.threads[thread_id].claude_instances.append(claude_instance)

        self._save_active_thread()
        self._save_threads()

    def list_threads(self, limit: int = 20) -> List[Thread]:
        """List recent threads"""
        threads = sorted(
            self.threads.values(),
            key=lambda t: t.updated_at,
            reverse=True
        )
        return threads[:limit]

    def export_thread(self, thread_id: str, output_path: str):
        """
        Export a thread for sharing

        Args:
            thread_id: Thread to export
            output_path: Where to save the export
        """
        thread = self.threads.get(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")

        with open(output_path, 'w') as f:
            json.dump(asdict(thread), f, indent=2)

        print(f"Thread exported to: {output_path}")

    def import_thread(self, input_path: str, claude_instance: str = "console") -> Thread:
        """
        Import a thread from another Claude instance

        Args:
            input_path: Path to exported thread
            claude_instance: Which instance is importing

        Returns:
            Imported thread
        """
        with open(input_path, 'r') as f:
            thread_data = json.load(f)

        thread = Thread(**thread_data)

        # Add importing instance to the list
        if claude_instance not in thread.claude_instances:
            thread.claude_instances.append(claude_instance)

        self.threads[thread.id] = thread
        self._save_threads()

        print(f"Thread '{thread.title}' imported successfully!")
        return thread

    def get_thread_summary(self, thread_id: Optional[str] = None) -> str:
        """Get a summary of a thread"""
        thread = self.get_thread(thread_id) if thread_id else self.get_active_thread()

        if not thread:
            return "No thread found"

        summary = []
        summary.append(f"Thread: {thread.title}")
        summary.append(f"ID: {thread.id}")
        summary.append(f"Created: {thread.created_at}")
        summary.append(f"Updated: {thread.updated_at}")
        summary.append(f"Messages: {len(thread.messages)}")
        summary.append(f"Claude Instances: {', '.join(thread.claude_instances)}")
        summary.append("")
        summary.append("Recent Messages:")

        for msg in thread.messages[-5:]:
            summary.append(f"  [{msg.role}] {msg.content[:100]}...")
            if msg.tools_used:
                summary.append(f"    Tools: {', '.join(msg.tools_used)}")

        return "\n".join(summary)

    def search_threads(self, query: str) -> List[Thread]:
        """Search threads by content or title"""
        query_lower = query.lower()
        results = []

        for thread in self.threads.values():
            # Search in title
            if query_lower in thread.title.lower():
                results.append(thread)
                continue

            # Search in messages
            for msg in thread.messages:
                if query_lower in msg.content.lower():
                    results.append(thread)
                    break

        return results

    def generate_context_for_claude(self, thread_id: Optional[str] = None,
                                   max_messages: int = 50) -> str:
        """
        Generate a context string to pass to a Claude instance

        Args:
            thread_id: Thread to generate context from
            max_messages: Maximum messages to include

        Returns:
            Formatted context string
        """
        thread = self.get_thread(thread_id) if thread_id else self.get_active_thread()

        if not thread:
            return ""

        context = []
        context.append(f"# Thread: {thread.title}")
        context.append(f"# Thread ID: {thread.id}")
        context.append(f"# Previous Claude instances: {', '.join(thread.claude_instances)}")
        context.append("")
        context.append("# Conversation History:")
        context.append("")

        for msg in thread.messages[-max_messages:]:
            context.append(f"## {msg.role.upper()}")
            context.append(msg.content)
            if msg.tools_used:
                context.append(f"*Tools used: {', '.join(msg.tools_used)}*")
            context.append("")

        return "\n".join(context)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Conversation Tracker")
    parser.add_argument('command', choices=[
        'create', 'add', 'list', 'show', 'switch', 'export', 'import',
        'search', 'context'
    ])
    parser.add_argument('--title', help='Thread title')
    parser.add_argument('--message', help='Message content')
    parser.add_argument('--thread-id', help='Thread ID')
    parser.add_argument('--file', help='File path for export/import')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--instance', default='cli', help='Claude instance name')

    args = parser.parse_args()

    tracker = ConversationTracker()

    if args.command == 'create':
        thread = tracker.create_thread(
            args.title or "New Conversation",
            args.message,
            args.instance
        )
        print(f"Created thread: {thread.id}")
        print(f"Title: {thread.title}")

    elif args.command == 'add':
        msg = tracker.add_message(
            args.message,
            role='user',
            thread_id=args.thread_id
        )
        print(f"Added message: {msg.id}")

    elif args.command == 'list':
        threads = tracker.list_threads()
        print(f"\nRecent Threads ({len(threads)}):\n")
        for t in threads:
            active = " [ACTIVE]" if t.id == tracker.active_thread_id else ""
            print(f"  {t.id}{active}")
            print(f"    Title: {t.title}")
            print(f"    Messages: {len(t.messages)}")
            print(f"    Updated: {t.updated_at}")
            print(f"    Instances: {', '.join(t.claude_instances)}")
            print()

    elif args.command == 'show':
        print(tracker.get_thread_summary(args.thread_id))

    elif args.command == 'switch':
        tracker.switch_thread(args.thread_id, args.instance)
        print(f"Switched to thread: {args.thread_id}")

    elif args.command == 'export':
        tracker.export_thread(
            args.thread_id or tracker.active_thread_id,
            args.file or f"thread_{args.thread_id}.json"
        )

    elif args.command == 'import':
        thread = tracker.import_thread(args.file, args.instance)
        print(f"Imported: {thread.title} ({thread.id})")

    elif args.command == 'search':
        results = tracker.search_threads(args.query)
        print(f"\nFound {len(results)} thread(s):\n")
        for t in results:
            print(f"  {t.id} - {t.title}")

    elif args.command == 'context':
        context = tracker.generate_context_for_claude(args.thread_id)
        print(context)


if __name__ == "__main__":
    main()
