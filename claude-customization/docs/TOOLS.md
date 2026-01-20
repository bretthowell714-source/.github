# Available Tools Reference

Complete reference of all tools available in Claude and how to use them effectively.

## Table of Contents

1. [File Operations](#file-operations)
2. [Search and Discovery](#search-and-discovery)
3. [Command Execution](#command-execution)
4. [Web Operations](#web-operations)
5. [Development Tools](#development-tools)
6. [Specialized Tools](#specialized-tools)

## File Operations

### Read

**Purpose**: Read file contents from the filesystem

**Parameters**:
- `file_path` (required): Absolute path to file
- `offset` (optional): Starting line number (default: 1)
- `limit` (optional): Number of lines to read

**Supported Formats**:
- Text files (.txt, .md, .json, .yaml, .xml, etc.)
- Code files (.js, .py, .go, .rs, .java, .ts, etc.)
- Images (.png, .jpg, .jpeg, .gif, .webp, etc.)
- PDFs (.pdf)
- Jupyter Notebooks (.ipynb)

**Examples**:

```bash
# Read entire file
claude-code read /path/to/file.txt

# Read specific lines
claude-code read /path/to/file.txt --offset 10 --limit 50

# Read image
claude-code read /path/to/image.png

# Read PDF
claude-code read /path/to/document.pdf

# Read Jupyter notebook
claude-code read /path/to/notebook.ipynb
```

**Best Practices**:
- Always use absolute paths
- For large files, use offset and limit
- Handle binary files appropriately
- Check file permissions before reading

### Write

**Purpose**: Create or overwrite files with content

**Parameters**:
- `file_path` (required): Absolute path to file
- `content` (required): File content to write

**Supported Operations**:
- Create new files
- Overwrite existing files
- Create directory structure as needed
- Preserve file permissions

**Examples**:

```bash
# Create new file
claude-code write /path/to/new-file.txt "File content here"

# Create JSON file
claude-code write /path/to/config.json '{"key": "value"}'

# Create from template
claude-code write /path/to/script.sh "#!/bin/bash\necho 'Hello'"
```

**Best Practices**:
- Use Edit tool for modifying existing files
- Always use absolute paths
- Backup important files before writing
- Verify content before writing
- Use git for version control

### Edit

**Purpose**: Perform targeted string replacements in files

**Parameters**:
- `file_path` (required): Absolute path to file
- `old_string` (required): Text to find and replace
- `new_string` (required): Replacement text
- `replace_all` (optional): Replace all instances (default: first only)

**Constraints**:
- Must read file first (safety requirement)
- `old_string` must be unique in file (or use `replace_all`)
- Preserves indentation and formatting
- Works on any text file

**Examples**:

```bash
# Replace single instance
claude-code edit /path/to/file.js \
  --old "const x = 1" \
  --new "const x = 2"

# Replace all instances
claude-code edit /path/to/file.js \
  --old "console.log" \
  --new "debug.log" \
  --replace-all

# Multi-line replacement
claude-code edit /path/to/file.py \
  --old "def old_function():\n    pass" \
  --new "def new_function():\n    return True"
```

**Best Practices**:
- Always read file first
- Use larger context to ensure uniqueness
- Make surgical edits, not bulk changes
- Commit changes to git
- Test edits before proceeding

### Glob

**Purpose**: Find files matching patterns

**Parameters**:
- `pattern` (required): Glob pattern (e.g., "**/*.js")
- `path` (optional): Directory to search (default: current)

**Pattern Examples**:
- `**/*.js` - All JavaScript files
- `src/**/*.tsx` - TypeScript React files in src
- `*.json` - JSON files in current directory
- `**/node_modules` - Node modules anywhere
- `test/**/*.test.js` - Test files

**Examples**:

```bash
# Find all TypeScript files
claude-code glob "**/*.ts"

# Find files in specific directory
claude-code glob "*.js" --path ./src

# Find test files
claude-code glob "**/*.test.{js,ts}"

# Find specific filename
claude-code glob "**/package.json"
```

**Best Practices**:
- Use specific patterns for faster results
- Exclude node_modules with negation patterns
- Combine with grep for content search
- Use for file discovery and analysis

## Search and Discovery

### Grep

**Purpose**: Search file contents using regex patterns

**Parameters**:
- `pattern` (required): Regex pattern to search
- `path` (optional): Files to search (default: current)
- `type` (optional): File type filter (js, py, rust, etc.)
- `glob` (optional): Glob pattern to filter files
- `output_mode` (optional): "content", "files_with_matches", or "count"
- `-i` (optional): Case-insensitive search
- `-n` (optional): Show line numbers (default: true)
- `-A/-B/-C` (optional): Context lines (after/before/both)

**Examples**:

```bash
# Search for pattern
claude-code grep "function.*async"

# Case-insensitive search
claude-code grep "import" -i

# Search only JavaScript files
claude-code grep "console.log" --type js

# Show context
claude-code grep "error" -C 3

# Count matches
claude-code grep "todo" --output-mode count

# Filter by glob pattern
claude-code grep "api" --glob "**/*.ts"

# Show files with matches only
claude-code grep "deprecated" --output-mode files_with_matches
```

**Best Practices**:
- Use specific patterns to reduce noise
- Filter by file type for precision
- Use context to understand matches
- Combine with other tools for analysis

## Command Execution

### Bash

**Purpose**: Execute shell commands and scripts

**Parameters**:
- `command` (required): Shell command to execute
- `description` (optional): Command description (5-10 words)
- `timeout` (optional): Timeout in milliseconds (default: 120000, max: 600000)
- `run_in_background` (optional): Run as background task

**Supported Operations**:
- Shell scripts
- System commands
- Git operations
- Package management
- File operations
- Build commands
- Testing

**Examples**:

```bash
# Simple command
claude-code bash "ls -la"

# Git operations
claude-code bash "git status"
claude-code bash "git commit -m 'Fix bug'"

# Chain commands
claude-code bash "npm install && npm run build"

# Background task
claude-code bash "npm test" --run-in-background

# With timeout
claude-code bash "long-running-task" --timeout 300000
```

**Best Practices**:
- Quote file paths with spaces
- Use absolute paths when possible
- Chain commands with && for dependencies
- Use background execution for long tasks
- Check exit codes for errors
- Avoid destructive operations without confirmation

## Web Operations

### WebFetch

**Purpose**: Fetch and analyze web content

**Parameters**:
- `url` (required): Full URL to fetch
- `prompt` (required): What to extract/analyze

**Features**:
- HTML to markdown conversion
- Content extraction
- AI-powered analysis
- 15-minute caching
- Redirect handling (up to 5 redirects)

**Examples**:

```bash
# Fetch and extract
claude-code fetch \
  --url "https://example.com/api-docs" \
  --prompt "What are the main API endpoints?"

# Fetch and summarize
claude-code fetch \
  --url "https://example.com/article" \
  --prompt "Summarize the main points"

# Extract specific information
claude-code fetch \
  --url "https://example.com/pricing" \
  --prompt "What are the pricing plans and costs?"
```

**Best Practices**:
- Use specific prompts for relevant results
- Handle redirects automatically
- Cache results locally when needed
- Respect rate limiting
- Verify content accuracy

### WebSearch

**Purpose**: Search the web for information

**Parameters**:
- `query` (required): Search query
- `allowed_domains` (optional): Only include specific domains
- `blocked_domains` (optional): Exclude specific domains

**Features**:
- Real-time search results
- Domain filtering
- Up-to-date information
- Context-aware results

**Examples**:

```bash
# Basic search
claude-code search "latest Node.js features 2026"

# Domain-specific search
claude-code search "React hooks tutorial" \
  --allowed-domains react.dev,reactjs.org

# Exclude domains
claude-code search "python async" \
  --blocked-domains stackoverflow.com
```

**Best Practices**:
- Use current year in search queries
- Be specific in search terms
- Filter by domain for relevant results
- Use recent information for current topics

## Development Tools

### NotebookEdit

**Purpose**: Edit Jupyter notebook cells

**Parameters**:
- `notebook_path` (required): Path to .ipynb file
- `cell_number` (required): Cell index (0-indexed)
- `new_source` (required): New cell content
- `cell_type` (optional): "code" or "markdown"
- `edit_mode` (optional): "replace", "insert", or "delete"

**Examples**:

```bash
# Replace cell content
claude-code notebook-edit \
  --notebook /path/to/notebook.ipynb \
  --cell 0 \
  --new-source "import pandas as pd"

# Insert new cell
claude-code notebook-edit \
  --notebook /path/to/notebook.ipynb \
  --cell 0 \
  --cell-type code \
  --edit-mode insert \
  --new-source "print('Hello')"

# Delete cell
claude-code notebook-edit \
  --notebook /path/to/notebook.ipynb \
  --cell 5 \
  --edit-mode delete
```

**Best Practices**:
- Backup notebooks before editing
- Use cell indexes carefully (0-indexed)
- Preserve cell outputs when appropriate
- Test notebook execution after edits

## Specialized Tools

### Task Management

**Purpose**: Manage background tasks and agents

**Parameters**:
- `task_id` (required): Task identifier
- `block` (optional): Wait for completion (default: true)
- `timeout` (optional): Maximum wait time

**Examples**:

```bash
# Get task output
claude-code task-output --task-id abc123

# Non-blocking check
claude-code task-output --task-id abc123 --block=false

# With timeout
claude-code task-output --task-id abc123 --timeout 60000
```

## Tool Combination Patterns

### Pattern 1: Code Discovery and Analysis

```
1. Glob: Find files matching pattern
2. Grep: Search content in found files
3. Read: Read specific files for details
4. Edit: Make targeted changes
```

### Pattern 2: Documentation Research

```
1. WebSearch: Find relevant resources
2. WebFetch: Get detailed information
3. Write: Create documentation
4. Read: Verify content
```

### Pattern 3: Development Workflow

```
1. Read: Understand current code
2. Plan: Design changes
3. Edit/Write: Implement changes
4. Bash: Run tests
5. Bash: Commit and push
```

### Pattern 4: Data Processing

```
1. Read: Load data file
2. Bash: Process with command-line tools
3. Write: Save results
4. WebFetch: Get additional data if needed
```

## Tool Efficiency Tips

1. **Combine operations**: Use patterns to accomplish multiple steps
2. **Parallel execution**: Run independent tools simultaneously
3. **Caching**: WebFetch caches for 15 minutes
4. **Batch operations**: Process multiple files efficiently
5. **Error handling**: Check tool results for errors before proceeding

## Tool Limitations

| Tool | Max Size | Timeout | Rate Limit |
|------|----------|---------|-----------|
| Read | System dependent | 30s | None |
| Write | System dependent | 30s | None |
| Bash | Output: 30KB | 2m default, 10m max | Per operation |
| WebFetch | Content: Varies | 30s | External service |
| WebSearch | Varies | 30s | US only |
| Glob | Files: Unlimited | 5s | None |
| Grep | Files: Unlimited | 10s | None |

---

## See Also

- [CAPABILITIES.md](./CAPABILITIES.md) - Overview of capabilities
- [CUSTOM_TOOLS.md](./CUSTOM_TOOLS.md) - Creating custom tools
- [OPTIMIZATION.md](./OPTIMIZATION.md) - Performance optimization

Last updated: January 2026
