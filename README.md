# Claude Integrations Toolkit 🚀

**The complete toolkit for connecting Claude across all platforms with self-learning capabilities!**

[![Tests](https://github.com/your-repo/.github/actions/workflows/test-integrations.yml/badge.svg)](https://github.com/your-repo/.github/actions)

## 🎯 What Is This?

A comprehensive integration system that enables:

1. **File Upload & Management** - Upload files to Anthropic Files API
2. **Self-Embedding Meta-Skill System** - AI that learns and improves itself
3. **Multi-Instance Threading** - Share conversations across Claude instances
4. **API Usage Tracking** - Stay within rate limits and budgets
5. **MCP Servers** - Model Context Protocol integrations
6. **Cross-Platform** - Works on Desktop, Web, VSCode, Mobile, Docker

## 📦 Components

### 1. Python Client (`python-client/`)
- **File Upload Client** - Upload/manage files via Anthropic API
- **Conversation Tracker** - Track and share conversations
- **API Usage Tracker** - Monitor usage and enforce limits
- **Tracked API Client** - Automatic usage monitoring

### 2. Meta-Skill Engine (`meta-skill/`)
- **Self-Embedding System** - Learns new skills automatically
- **Knowledge Base** - Accumulates knowledge across sessions
- **Pattern Learning** - Identifies successful patterns
- **Auto-Update** - Skills improve through usage

### 3. MCP Servers (`mcp-servers/`)
- **File Upload MCP** - Expose file upload tools
- **Meta-Skill MCP** - Self-learning capabilities via MCP
- **Conversation Tracker MCP** - Thread management via MCP

### 4. Docker (`docker/`)
- **Dockerfile** - Containerized integrations
- **docker-compose.yml** - Multi-service deployment

### 5. VSCode Integration (`.vscode/`)
- **MCP Configuration** - Pre-configured for VSCode
- **Settings** - Optimized settings

### 6. GitHub Actions (`.github/workflows/`)
- **CI/CD** - Automated testing
- **Integration Tests** - Verify all components work

## 🚀 Quick Start

### Option 1: Docker (Easiest)

```bash
# Clone repo
git clone https://github.com/your-repo/.github.git
cd .github

# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r python-client/requirements.txt
pip install -r meta-skill/requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# Test the meta-skill system
cd meta-skill/tests
python3 test_meta_skill_engine.py
```

### Option 3: MCP Servers

**Claude Desktop Config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "file-upload": {
      "command": "python3",
      "args": ["/path/to/.github/mcp-servers/file-upload-mcp/server.py"],
      "env": {"ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"}
    },
    "meta-skill": {
      "command": "python3",
      "args": ["/path/to/.github/mcp-servers/meta-skill-mcp/server.py"]
    },
    "conversation-tracker": {
      "command": "python3",
      "args": ["/path/to/.github/mcp-servers/conversation-tracker-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop and you'll have new tools available!

## 📚 Documentation

- [Python Client README](python-client/README.md)
- [Meta-Skill Engine README](meta-skill/README.md)
- [MCP Servers README](mcp-servers/README.md)
- [Conversation Tracker Guide](python-client/CONVERSATION_TRACKER_README.md)
- [Docker Setup](docker/README.md)

## 💡 Use Cases

### 1. File Upload to Claude

```python
from claude_files_api import ClaudeFilesAPI

client = ClaudeFilesAPI()
result = client.upload_file("/path/to/document.pdf")
print(f"File ID: {result['id']}")
```

### 2. Self-Learning System

```python
from meta_skill_engine import MetaSkillEngine, Skill

engine = MetaSkillEngine()

# Embed a new skill
skill = Skill(
    name="api_integration",
    description="Integrate with APIs",
    category="integration",
    patterns=["api", "integrate", "connect"]
)
engine.embed_skill(skill)

# Get recommendations
recs = engine.get_recommendations("How do I integrate with an API?")
print(recs)  # ['api_integration', ...]
```

### 3. Multi-Instance Threading

```python
from conversation_tracker import ConversationTracker

tracker = ConversationTracker()

# Create thread
thread = tracker.create_thread(
    title="My Project",
    initial_message="Let's build an API",
    claude_instance="console"
)

# Export for another instance
tracker.export_thread(thread.id, "my_thread.json")

# Import on Desktop/VSCode/Mobile
tracker.import_thread("my_thread.json", claude_instance="desktop")
```

### 4. API Usage Monitoring

```python
from claude_api_client_with_tracking import TrackedClaudeClient

client = TrackedClaudeClient()

# Check budget before calling
budget = client.get_remaining_budget()
print(f"Daily budget remaining: ${budget['daily_budget_remaining']:.2f}")

# Make tracked API call
response = client.create_message(
    model="claude-sonnet-4",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Get usage report
print(client.get_usage_report('today'))
```

## 🔧 Platform Setup

### Windows

```powershell
# Set API key
$env:ANTHROPIC_API_KEY = "your-key"

# Install
pip install -r python-client\requirements.txt

# Configure Claude Desktop
copy mcp-servers\claude_desktop_config.json $env:APPDATA\Claude\
```

### macOS

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Install
pip install -r python-client/requirements.txt

# Configure Claude Desktop
cp mcp-servers/claude_desktop_config.json ~/Library/Application\ Support/Claude/
```

### Linux

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Install
pip install -r python-client/requirements.txt

# Configure Claude Desktop
mkdir -p ~/.config/Claude
cp mcp-servers/claude_desktop_config.json ~/.config/Claude/
```

### VSCode

1. Open workspace in VSCode
2. Install Claude extension
3. MCP servers auto-configured from `.vscode/settings.json`

### Mobile (Android/iOS)

Use conversation tracker CLI to export threads, then:
- Share via cloud storage
- Email to yourself
- Use QR code sharing

Paste context into mobile Claude app.

## 🧪 Testing

### Run All Tests

```bash
# Meta-skill tests
cd meta-skill/tests
./run_tests.sh

# Or directly
python3 test_meta_skill_engine.py
```

### CI/CD

Tests run automatically on push via GitHub Actions.

## 📊 Features

### ✅ File Upload & Management
- Upload any file type
- List/get/delete files
- Download file content
- Full API coverage

### ✅ Self-Embedding Meta-Skill System
- Auto-discovers skills from web content
- Learns from conversations
- Persists knowledge across sessions
- Auto-updates based on usage
- Export/import configurations

### ✅ Multi-Instance Threading
- Share conversations across platforms
- Export/import threads
- Track which instances accessed threads
- Generate context for Claude

### ✅ API Usage Tracking
- Rate limit enforcement
- Budget tracking (daily/monthly)
- Cost estimation
- Usage reports
- Alert system

### ✅ MCP Integration
- 3 custom MCP servers
- Works with Claude Desktop/VSCode
- Pre-configured setups
- Docker deployment

## 🔐 Security

- **NEVER** commit API keys
- Use environment variables
- Secure secret management
- Input validation
- Rate limiting

## 🤝 Contributing

1. Fork repo
2. Create feature branch
3. Add tests
4. Submit PR

## 📄 License

MIT License - See LICENSE file

## 🆘 Support

- [GitHub Issues](https://github.com/your-repo/.github/issues)
- [Documentation](docs/)
- [Examples](examples/)

## 🌟 Star History

If this helped you, give it a star! ⭐

## 📈 Roadmap

- [ ] Node.js/TypeScript client
- [ ] Mobile SDKs (iOS/Android)
- [ ] Web dashboard
- [ ] Real-time sync
- [ ] Advanced analytics
- [ ] Multi-model support

---

**Built with ❤️ for the Claude community**

*Connecting Claude across all platforms with self-learning capabilities*
