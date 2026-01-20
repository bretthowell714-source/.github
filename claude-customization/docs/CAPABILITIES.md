# Claude's Built-in Capabilities

Comprehensive documentation of Claude's native capabilities and features available for customization.

## Overview

Claude provides multiple interfaces and capabilities for software engineering tasks, file operations, web access, and more. This document outlines all available capabilities.

## Core Capabilities

### 1. File Operations

**Read Files**
- Read any file from the filesystem
- Support for text, binary, images, PDFs, and Jupyter notebooks
- Configurable line offset and limit for large files
- Returns content with line numbers

```
Tool: Read
Usage: Read file contents directly by path
```

**Write Files**
- Create or overwrite files
- Support for any file type
- Automatic file creation
- Permission-aware writing

```
Tool: Write
Usage: Write or create files with specified content
```

**Edit Files**
- Exact string replacement in files
- Preserve indentation and formatting
- Replace single or multiple instances
- Read-first requirement for safety

```
Tool: Edit
Usage: Modify existing files with targeted edits
```

**File Search**
- Fast pattern matching with glob patterns
- Search by file name and extension
- Recursive directory searching
- Returns sorted results

```
Tool: Glob
Usage: Find files by pattern matching
```

### 2. Content Search

**Grep/Ripgrep**
- Full regex pattern support
- Case-sensitive and case-insensitive search
- File type filtering
- Context lines (before/after matches)
- Line numbering

```
Tool: Grep
Usage: Search file contents with regex patterns
```

### 3. Command Execution

**Bash**
- Execute shell commands
- Run scripts and binaries
- Git operations
- Background command execution with timeout
- Proper quoting and escaping

```
Tool: Bash
Usage: Execute terminal commands and scripts
```

**Git Operations**
- Clone, commit, push, pull
- Branch management
- Diff and status
- Merge and rebase
- Tag management

```
Bash subset: git commands
Usage: Version control operations
```

### 4. Web Operations

**Web Fetch**
- Fetch and analyze web content
- HTML to markdown conversion
- Content extraction with prompts
- Self-cleaning cache (15 minutes)
- Redirect handling

```
Tool: WebFetch
Usage: Retrieve and process web content
```

**Web Search**
- Real-time web search
- Search result filtering
- Domain inclusion/exclusion
- Context-aware results
- Up-to-date information retrieval

```
Tool: WebSearch
Usage: Search the web for information
```

## Specialized Tools

### 5. Notebook Operations

**Jupyter Notebook Edit**
- Read/write Jupyter notebooks (.ipynb)
- Cell-level editing
- Cell insertion and deletion
- Support for code and markdown cells
- Output preservation

```
Tool: NotebookEdit
Usage: Edit specific cells in Jupyter notebooks
```

## Advanced Capabilities

### 6. Specialized Agents

**General-Purpose Agent**
- Multi-step task execution
- Complex problem solving
- Research and execution
- Tool orchestration

```
Subagent: general-purpose
Usage: Complex, multi-step tasks
```

**Explore Agent**
- Fast codebase exploration
- Pattern-based file finding
- Code analysis
- Codebase structure understanding
- Multiple search rounds

```
Subagent: Explore
Usage: Quick codebase navigation and analysis
```

**Plan Agent**
- Software architecture planning
- Implementation strategy design
- Critical file identification
- Architectural trade-off analysis

```
Subagent: Plan
Usage: Design implementation strategies
```

**Bash Agent**
- Command execution specialist
- Shell operations
- Script execution
- Terminal-based tasks

```
Subagent: Bash
Usage: Terminal and shell command execution
```

**StatusLine Setup Agent**
- Claude Code configuration
- Status line customization
- Settings management

```
Subagent: statusline-setup
Usage: Configure Claude Code settings
```

### 7. MCP Server Support

**Model Context Protocol**
- Connect to MCP servers
- Extend tool availability
- Custom resource access
- Standardized tool definitions

```
Feature: MCP Servers
Usage: Connect to custom MCP implementations
```

## Claude Code CLI Features

### 8. Session Management

- **SessionStart Hooks**: Execute commands before sessions
- **Pre-commit Hooks**: Validate code before commits
- **Build Validation**: Automated build verification
- **Test Running**: Integrated test execution

### 9. Configuration

**Claude Code Settings**
- Model selection
- System prompts
- Tool configuration
- Workspace settings
- Hook management

```
Tool: statusline-setup
Usage: Configure Claude Code settings
```

## Claude Agent SDK

### 10. Custom Agent Development

**Agent Creation**
- Define custom agents
- Tool selection per agent
- System prompt customization
- Response formatting
- Multi-turn conversations

**Tool Definition**
- Schema-based tool definitions
- Parameter validation
- Type checking
- Documentation generation

**Execution Control**
- Token budgets
- Timeout management
- Retry logic
- Error handling

## Task Management

### 11. Background Task Execution

**Async Execution**
- Run tools in background
- Task ID tracking
- Output file retrieval
- Timeout configuration
- Status monitoring

```
Tool: TaskOutput
Usage: Monitor and retrieve background task results
```

**Task Control**
- Background shell execution
- Agent spawning
- Task monitoring
- Resource management

## Knowledge and Context

### 12. Web-Connected Knowledge

**Real-time Information**
- Current date awareness (updated daily)
- Web search for recent information
- Knowledge cutoff: February 2025
- Frontier model awareness

**Contextual Processing**
- Conversation history
- Message summarization
- Context preservation
- Long conversation support

## Customization Capabilities

### 13. System Prompts

- Override default behavior
- Custom instructions
- Role definition
- Output formatting
- Tone and style customization

### 14. Tool Addition

- Create custom tools
- Tool schema definition
- Parameter validation
- Tool registration
- Tool composition

### 15. Plugin System

- Extend functionality
- Hook into Claude processes
- Custom workflows
- Integration points

## Security Features

### 16. Sandboxing

- Safe command execution
- File operation restrictions
- Network request filtering
- Permission validation
- Resource limits

### 17. Verification

- Git safety protocols
- Commit verification
- Hook execution
- Code review capabilities

## Performance Features

### 18. Optimization

- Parallel tool execution
- Caching (15-minute web cache)
- Streaming responses
- Token budget management
- Efficient file handling

## Integration Points

### 19. External Integrations

**GitHub**
- Repository operations (via gh CLI)
- Pull request management
- Issue tracking
- GitHub Actions integration

**API Integrations**
- Anthropic API
- Custom REST APIs
- Third-party service connection
- Webhook support

**Data Sources**
- File systems
- Databases (via tools)
- Web APIs
- Streams and pipes

## Capability Combinations

### 20. Powerful Combinations

**Development Workflows**
- Read → Analyze → Edit → Commit → Push
- Explore → Plan → Implement → Test → Deploy
- Search → Research → Document → Publish

**Data Processing**
- Read → Process → Write → Verify
- Fetch → Parse → Transform → Export

**Automation**
- Monitor → Analyze → Execute → Report
- Schedule → Execute → Log → Alert

## Limitations and Boundaries

### 21. Known Limitations

**File Operations**
- Maximum file size: System dependent
- Binary file support: Limited
- Permission restrictions: Honor filesystem permissions

**Web Operations**
- Rate limiting: Apply external service limits
- HTTPS requirement: Enforced
- Redirect handling: Up to 5 redirects

**Command Execution**
- Timeout: 2 minutes default (max 10 minutes)
- No interactive input: Scripted operations only
- Sandboxed environment: No direct system access

**Parallelization**
- Maximum concurrent operations: System dependent
- Rate limiting: Per-operation basis
- Resource constraints: Memory and CPU

## Best Practices

### 22. Capability Usage Guidelines

**File Operations**
- Use glob for searching, grep for content
- Batch edits efficiently
- Verify before modifying
- Use git for version control

**Web Operations**
- Use WebSearch for current info
- Use WebFetch for specific content
- Cache results locally when appropriate
- Handle redirects gracefully

**Command Execution**
- Use bash for system commands
- Prefer tool alternatives when available
- Handle errors gracefully
- Log important operations

**Task Management**
- Use background execution for long tasks
- Monitor task status
- Clean up resources
- Handle timeouts

---

## See Also

- [TOOLS.md](./TOOLS.md) - Detailed tool documentation
- [CUSTOM_TOOLS.md](./CUSTOM_TOOLS.md) - Creating custom tools
- [PLUGINS.md](./PLUGINS.md) - Plugin development
- [API Documentation](https://docs.anthropic.com)

Last updated: January 2026
