# Claude Conversation Tracker & Multi-Instance Threading

**Connect conversations across all your Claude instances!**

## 🎯 What Is This?

A system that lets you:
- **Track conversations** across console.anthropic.com, Desktop, VSCode, Mobile
- **Share threads** between Claude instances
- **Continue conversations** from any platform
- **Sync context** automatically

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Create Your First Thread

```bash
# From console.anthropic.com or any Claude instance
python3 conversation_tracker.py create \
  --title "My Project Discussion" \
  --message "Let's build an API integration" \
  --instance "console"
```

### Add Messages

```bash
python3 conversation_tracker.py add \
  --message "I need help with file uploads"
```

### List All Threads

```bash
python3 conversation_tracker.py list
```

Output:
```
Recent Threads (3):

  abc-123-def [ACTIVE]
    Title: My Project Discussion
    Messages: 15
    Updated: 2026-01-01T10:30:00
    Instances: console, desktop, vscode

  xyz-789-ghi
    Title: Docker Setup
    Messages: 8
    Updated: 2026-01-01T09:15:00
    Instances: console
```

## 🔗 Connecting Claude Instances

### From Console → Desktop

**In console.anthropic.com:**
```bash
# Export thread
python3 conversation_tracker.py export \
  --thread-id abc-123-def \
  --file ~/Downloads/my_thread.json
```

**In Claude Desktop:**
```bash
# Import thread
python3 conversation_tracker.py import \
  --file ~/Downloads/my_thread.json \
  --instance "desktop"

# Switch to it
python3 conversation_tracker.py switch --thread-id abc-123-def
```

**Now continue the conversation in Desktop!**

### From Desktop → Mobile (via Cloud)

1. Export from Desktop
2. Upload to cloud storage (Dropbox, Drive, etc.)
3. Download on mobile
4. Import into mobile Claude app

### Using MCP Server (Automatic)

**Add to your MCP config:**

```json
{
  "mcpServers": {
    "conversation-tracker": {
      "command": "python3",
      "args": [
        "/home/user/.github/mcp-servers/conversation-tracker-mcp/server.py"
      ]
    }
  }
}
```

**Then in any Claude instance:**

- "Create a new thread called 'API Development'"
- "Add this message to the thread"
- "Show me all my threads"
- "Switch to thread abc-123"
- "Get the context from my previous thread"

## 📱 Platform-Specific Setup

### Console (console.anthropic.com)

```bash
# Set up tracker
cd ~/.github/python-client
python3 conversation_tracker.py create --title "Console Thread" --instance "console"

# Use in your prompts
python3 conversation_tracker.py context | pbcopy  # macOS
# Then paste into Claude console
```

### Claude Desktop

```bash
# Add MCP server to config
# Location: ~/Library/Application Support/Claude/claude_desktop_config.json

{
  "mcpServers": {
    "conversation-tracker": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/conversation-tracker-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. Now you have tools:
- `create_thread`
- `add_message`
- `list_threads`
- `switch_thread`
- `get_thread_context`

### VSCode

Add to `.vscode/settings.json`:
```json
{
  "claude.mcpServers": {
    "conversation-tracker": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/conversation-tracker-mcp/server.py"]
    }
  }
}
```

### Android/Mobile

Use the CLI to export threads:
```bash
python3 conversation_tracker.py export --file thread.json
```

Share via:
- Email to yourself
- Cloud storage
- Airdrop/Nearby Share

Then paste context into mobile Claude app.

## 💡 Use Cases

### 1. Continue Desktop Work on Mobile

```bash
# On desktop - export your thread
python3 conversation_tracker.py export \
  --file ~/Dropbox/claude_thread.json

# On mobile - open Dropbox, copy content
# Paste into Claude mobile with:
# "Here's my previous conversation context: [paste]"
```

### 2. Team Collaboration

```bash
# Person A exports thread
python3 conversation_tracker.py export --file team_discussion.json

# Person B imports it
python3 conversation_tracker.py import --file team_discussion.json

# Both can now continue the same conversation!
```

### 3. Project Continuity

```bash
# Monday - Start on console
python3 conversation_tracker.py create --title "Week 1: API Design"

# Tuesday - Continue on Desktop
python3 conversation_tracker.py switch --thread-id <id> --instance "desktop"

# Wednesday - Review on mobile
python3 conversation_tracker.py context --thread-id <id> > context.txt
# Send context.txt to mobile
```

## 🔍 Advanced Features

### Search Threads

```bash
python3 conversation_tracker.py search --query "Docker"
```

### Get Context for Claude

```bash
# Generate formatted context
python3 conversation_tracker.py context --thread-id abc-123

# Output:
# Thread: My Project Discussion
# Thread ID: abc-123-def
# Previous Claude instances: console, desktop
#
# Conversation History:
#
# USER
# Let's build an API integration
# ...
```

### Thread Summary

```bash
python3 conversation_tracker.py show --thread-id abc-123
```

## 🔧 API Usage

### In Python

```python
from conversation_tracker import ConversationTracker

tracker = ConversationTracker()

# Create thread
thread = tracker.create_thread(
    title="API Development",
    initial_message="Starting API work",
    claude_instance="console"
)

# Add messages
tracker.add_message(
    content="How do I upload files?",
    role="user",
    tools_used=["file_upload"]
)

tracker.add_message(
    content="Here's how to upload files...",
    role="assistant"
)

# Get context for Claude
context = tracker.generate_context_for_claude(thread.id)
print(context)

# Export for sharing
tracker.export_thread(thread.id, "my_thread.json")
```

### With MCP Server

```python
# In Claude (any instance with MCP enabled):

"""
Create a thread called "Docker Setup"
Add message: "I need to configure Docker"
List all my threads
Switch to the Docker thread
Get the full context from my API Development thread
"""
```

## 📊 Data Storage

Threads stored in: `~/.claude_threads/`

```
~/.claude_threads/
├── threads.json          # All threads
├── active_thread.json    # Current active thread
└── exports/              # Exported threads
```

## 🔐 Security & Privacy

- All data stored locally
- No cloud sync (you control sharing)
- Export/import is manual (secure)
- No API calls for tracking

## 🎨 Integration with Meta-Skill System

```python
from conversation_tracker import ConversationTracker
from meta_skill_engine import MetaSkillEngine

tracker = ConversationTracker()
engine = MetaSkillEngine()

# Track learning per thread
thread = tracker.get_active_thread()
for msg in thread.messages:
    if msg.tools_used:
        # Learn from tool usage in this thread
        engine.record_interaction(...)
```

## 📱 Mobile-Specific Tips

### Quick Context Sharing

```bash
# Create a short context file
python3 conversation_tracker.py context \
  --thread-id abc-123 > context.txt

# Email it to yourself
mail -s "Claude Context" you@email.com < context.txt
```

### Voice-to-Thread

1. Use voice input on mobile to add message
2. Export thread
3. Import on desktop to continue with coding tools

## 🚀 Future Enhancements

- [ ] Cloud sync (optional)
- [ ] Real-time collaboration
- [ ] Thread merging
- [ ] Auto-summarization
- [ ] Voice memo integration
- [ ] Attachment support

## 🆘 Troubleshooting

### Thread Not Found

```bash
# List all threads to find ID
python3 conversation_tracker.py list
```

### Import Fails

```bash
# Check file format
cat thread.json | jq .
```

### MCP Server Not Working

```bash
# Test server standalone
python3 server.py
# Send test: {"jsonrpc":"2.0","method":"tools/list","id":1}
```

## 📚 Examples

See `examples/` directory for:
- Console → Desktop workflow
- Team collaboration setup
- Project continuity examples
- Mobile integration

---

**Now you can seamlessly continue conversations across all Claude instances!** 🎉
