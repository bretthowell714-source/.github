# Available Tools & Capabilities

**Complete registry of all Claude tools, skills, and integrations**

## 🛠️ MCP Tools (Model Context Protocol)

### File Upload Tools
**Server:** `file-upload-mcp`
**Location:** `mcp-servers/file-upload-mcp/server.py`

| Tool | Description | Parameters |
|------|-------------|------------|
| `upload_file` | Upload file to Anthropic Files API | `file_path`, `purpose` |
| `list_files` | List all uploaded files | None |
| `delete_file` | Delete a file | `file_id` |

### Meta-Skill Engine Tools
**Server:** `meta-skill-mcp`
**Location:** `mcp-servers/meta-skill-mcp/server.py`

| Tool | Description | Parameters |
|------|-------------|------------|
| `embed_skill` | Add new skill to system | `name`, `description`, `category`, `patterns`, `tools` |
| `get_recommendations` | Get skill recommendations | `query` |
| `record_learning` | Record learned knowledge | `query`, `tools_used`, `knowledge` |
| `generate_report` | Generate skills report | None |
| `export_config` | Export system config | `output_path` |

### Conversation Tracker Tools
**Server:** `conversation-tracker-mcp`
**Location:** `mcp-servers/conversation-tracker-mcp/server.py`

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_thread` | Create conversation thread | `title`, `initial_message`, `claude_instance` |
| `add_message` | Add message to thread | `content`, `role`, `tools_used` |
| `list_threads` | List all threads | None |
| `switch_thread` | Switch active thread | `thread_id`, `claude_instance` |
| `get_thread_context` | Get thread context | `thread_id`, `max_messages` |
| `search_threads` | Search threads | `query` |
| `export_thread` | Export thread | `thread_id`, `output_path` |
| `import_thread` | Import thread | `input_path`, `claude_instance` |

## 🐍 Python Libraries

### File Upload Client
**Module:** `python-client/claude_files_api.py`

```python
from claude_files_api import ClaudeFilesAPI

client = ClaudeFilesAPI()
client.upload_file(path)
client.list_files()
client.get_file(file_id)
client.delete_file(file_id)
client.get_file_content(file_id)
```

### Meta-Skill Engine
**Module:** `meta-skill/core/meta_skill_engine.py`

```python
from meta_skill_engine import MetaSkillEngine, Skill

engine = MetaSkillEngine()
engine.embed_skill(skill)
engine.get_recommendations(query)
engine.record_interaction(context)
engine.generate_skill_report()
```

### Conversation Tracker
**Module:** `python-client/conversation_tracker.py`

```python
from conversation_tracker import ConversationTracker

tracker = ConversationTracker()
tracker.create_thread(title)
tracker.add_message(content)
tracker.export_thread(thread_id, path)
tracker.import_thread(path)
```

### API Usage Tracker
**Module:** `python-client/api_usage_tracker.py`

```python
from api_usage_tracker import APIUsageTracker

tracker = APIUsageTracker()
tracker.record_call(endpoint, model, input_tokens, output_tokens)
tracker.can_make_request(estimated_tokens)
tracker.get_usage_stats(period)
tracker.generate_report(period)
```

### Tracked Claude Client
**Module:** `python-client/claude_api_client_with_tracking.py`

```python
from claude_api_client_with_tracking import TrackedClaudeClient

client = TrackedClaudeClient()
response = client.create_message(model, max_tokens, messages)
budget = client.get_remaining_budget()
```

## 🧠 Meta-Skills (Auto-Learned)

Current skills in the system:

| Skill | Category | Patterns | Tools |
|-------|----------|----------|-------|
| `file_upload` | api_integration | upload, file, api | requests, anthropic_api |
| `web_research` | research | search, research, find | web_search, web_fetch |
| `code_generation` | development | create, build, implement | write, edit |
| `mcp_integration` | integration | mcp, tool, server | mcp_client |
| `self_embedding` | meta | learn, embed, update | yaml, json, file_operations |

**Note:** System learns new skills automatically from usage!

## 📱 Platform Support

### Claude Desktop
**Config:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Tools Available:** All MCP tools

### VSCode
**Config:** `.vscode/settings.json`
**Tools Available:** All MCP tools

### Console (console.anthropic.com)
**Usage:** Export context from tracker, paste into console
**Tools Available:** All Python libraries (via CLI)

### Mobile (Android/iOS)
**Usage:** Import/export threads
**Tools Available:** Context sharing only

### Docker
**Config:** `docker/docker-compose.yml`
**Tools Available:** All MCP servers as containers

## 🔧 CLI Commands

### File Upload
```bash
python3 python-client/claude_files_api.py upload --file document.pdf
python3 python-client/claude_files_api.py list
python3 python-client/claude_files_api.py delete --file-id abc-123
```

### Meta-Skill Engine
```bash
python3 meta-skill/core/meta_skill_engine.py init
python3 meta-skill/core/meta_skill_engine.py add-skill --name "my_skill" --category "custom"
python3 meta-skill/core/meta_skill_engine.py report
python3 meta-skill/core/meta_skill_engine.py export --file config.yaml
```

### Conversation Tracker
```bash
python3 python-client/conversation_tracker.py create --title "My Thread"
python3 python-client/conversation_tracker.py add --message "Hello"
python3 python-client/conversation_tracker.py list
python3 python-client/conversation_tracker.py export --file thread.json
```

### API Usage Tracker
```bash
python3 python-client/api_usage_tracker.py report
python3 python-client/api_usage_tracker.py check
python3 python-client/api_usage_tracker.py set-limits --daily-budget 10.00
```

## 🎯 Use Cases

### Upload File & Process
```bash
# Via MCP (in Claude Desktop)
upload_file(file_path="/path/to/doc.pdf")

# Via CLI
python3 python-client/claude_files_api.py upload --file doc.pdf
```

### Learn New Skill
```bash
# Via MCP
embed_skill(name="api_testing", description="Test APIs", category="testing")

# Via CLI
python3 meta-skill/core/meta_skill_engine.py add-skill --name "api_testing"
```

### Share Conversation Across Instances
```bash
# On Console
python3 python-client/conversation_tracker.py create --title "API Work"
python3 python-client/conversation_tracker.py export --file thread.json

# On Desktop (via MCP)
import_thread(input_path="thread.json", claude_instance="desktop")
```

### Monitor API Usage
```bash
# Check before making calls
python3 python-client/api_usage_tracker.py check

# View report
python3 python-client/api_usage_tracker.py report --period today
```

## 🔍 Tool Discovery

### Find Available Tools
```bash
# In Claude Desktop: Tools appear automatically in tool picker
# In VSCode: Use Claude extension tool palette
# Via CLI: Read this file!
```

### Add Custom Tools
1. Create MCP server in `mcp-servers/`
2. Add to `claude_desktop_config.json`
3. Restart Claude Desktop
4. Update this file!

## 📊 Tool Statistics

- **Total MCP Tools:** 16
- **Python Libraries:** 5
- **CLI Commands:** 20+
- **Meta-Skills:** 5+ (growing automatically!)
- **Platforms Supported:** 5

## 🔐 Required Environment Variables

```bash
# Required for file upload
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional for extended features
export GITHUB_TOKEN="ghp_..."
export BRAVE_API_KEY="..."
```

## 📚 Documentation

- [Main README](README.md)
- [Python Client](python-client/README.md)
- [Meta-Skill Engine](meta-skill/README.md)
- [MCP Servers](mcp-servers/README.md)
- [Conversation Tracker](python-client/CONVERSATION_TRACKER_README.md)

## ✅ Verification

Test all tools:
```bash
# Run comprehensive tests
cd meta-skill/tests && ./run_tests.sh

# Test MCP servers
python3 mcp-servers/file-upload-mcp/server.py &
python3 mcp-servers/meta-skill-mcp/server.py &

# Test CLI tools
python3 python-client/claude_files_api.py --help
python3 python-client/conversation_tracker.py --help
```

---

**Last Updated:** 2026-01-01
**Total Capabilities:** 40+ tools, skills, and integrations
**Status:** All systems operational ✅
