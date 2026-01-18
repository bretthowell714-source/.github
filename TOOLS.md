# Claude Code Tools

## Overview

This document describes the tools available to Claude Code and how to effectively use them in your development workflow.

## Built-in Tools

### File Operations

#### Read
- **Purpose**: Read file contents from the local filesystem
- **Usage**: Access any file directly, supports line offsets and limits for large files
- **Features**:
  - Reads images (PNG, JPG)
  - Reads PDFs with text and visual content extraction
  - Reads Jupyter notebooks (.ipynb) with all cells and outputs
  - Line numbers displayed in cat -n format

#### Write
- **Purpose**: Create new files or overwrite existing files
- **Usage**: Should read existing files first before overwriting
- **Best Practice**: Prefer editing over writing new files

#### Edit
- **Purpose**: Perform exact string replacements in files
- **Usage**: Must read file first, preserves exact indentation
- **Features**:
  - `replace_all` parameter for renaming across entire file
  - Fails if old_string is not unique (requires more context)

### Code Search

#### Glob
- **Purpose**: Fast file pattern matching
- **Usage**: Find files by name patterns (e.g., "**/*.js", "src/**/*.ts")
- **Returns**: Matching file paths sorted by modification time

#### Grep
- **Purpose**: Powerful content search built on ripgrep
- **Usage**: Search code with full regex syntax
- **Features**:
  - File filtering with glob or type parameters
  - Multiple output modes: content, files_with_matches, count
  - Context lines (-A, -B, -C flags)
  - Multiline matching support
  - Case-insensitive search (-i flag)

### Execution

#### Bash
- **Purpose**: Execute shell commands in persistent session
- **Usage**: Terminal operations (git, npm, docker, etc.)
- **Features**:
  - Optional timeout (up to 10 minutes)
  - Background execution support
  - Command chaining with && or ;
- **Important**: Use specialized tools for file operations, not bash commands

### Web Operations

#### WebSearch
- **Purpose**: Search the web for current information
- **Usage**: Access information beyond Claude's knowledge cutoff
- **Requirements**: MUST include sources section with links in responses

#### WebFetch
- **Purpose**: Fetch and analyze web content
- **Usage**: Retrieves URL content, converts HTML to markdown
- **Features**: 15-minute cache for faster repeated access

### Task Management

#### TodoWrite
- **Purpose**: Create and manage structured task lists
- **Usage**: Track progress on complex multi-step tasks
- **Task States**: pending, in_progress, completed
- **Best Practice**:
  - Update in real-time as you work
  - Only ONE task in_progress at a time
  - Mark completed immediately after finishing

#### Task
- **Purpose**: Launch specialized agents for complex tasks
- **Available Agents**:
  - general-purpose: Multi-step tasks and research
  - Explore: Fast codebase exploration
  - Plan: Implementation planning and architecture
  - claude-code-guide: Claude Code documentation lookup

### Jupyter Notebooks

#### NotebookEdit
- **Purpose**: Edit Jupyter notebook cells
- **Usage**: Replace, insert, or delete cells
- **Parameters**: notebook_path, cell_id, cell_type (code/markdown)

## Tool Usage Best Practices

### When to Use Each Tool

1. **File Search**: Use Glob for file patterns, Task tool for open-ended searches
2. **Content Search**: Use Grep for code search, avoid bash grep
3. **File Reading**: Use Read tool, not cat/head/tail commands
4. **File Editing**: Use Edit tool, not sed/awk commands
5. **File Creation**: Use Write tool, not echo or heredoc
6. **Codebase Exploration**: Use Task with Explore agent for thorough investigation

### Parallel vs Sequential Execution

- **Parallel**: Multiple independent tools in single message
  - Example: Reading multiple unrelated files
  - Example: Running git status and git diff

- **Sequential**: Dependent operations
  - Example: Write file then git commit
  - Example: mkdir then cp into new directory

### Optimization Tips

1. **Speculative Reads**: Read multiple potentially useful files in parallel
2. **Batch Operations**: Group independent tool calls together
3. **Use Specialized Tools**: Faster and more reliable than bash alternatives
4. **Avoid Redundancy**: Don't use bash for operations that have dedicated tools

## Tool Limitations

- **Read**: Line limit of 2000 lines per read, lines truncated at 2000 chars
- **Bash**: 2-minute default timeout, 10-minute maximum
- **WebFetch**: Results may be summarized for large content
- **Grep**: Default head_limit varies (0, 20, or 100 based on configuration)

## Security Considerations

- Bash commands execute with proper sandboxing
- File operations have appropriate permission checks
- Web operations are read-only
- Never commit sensitive files (.env, credentials, etc.)

## Examples

### File Pattern Search
```
Glob: pattern="**/*.test.ts"
```

### Content Search with Context
```
Grep: pattern="function\s+\w+", glob="*.js", output_mode="content", -C=3
```

### Reading Multiple Files
```
Read: file_path="/path/to/file1.ts"
Read: file_path="/path/to/file2.ts"
(in parallel)
```

### Task Tracking
```
TodoWrite: [
  {content: "Fix bug in auth", status: "in_progress", activeForm: "Fixing bug in auth"},
  {content: "Add tests", status: "pending", activeForm: "Adding tests"}
]
```

## Resources

- Use `/help` command for interactive assistance
- Report issues at https://github.com/anthropics/claude-code/issues
- See CLAUDE.MD for general project guidelines
