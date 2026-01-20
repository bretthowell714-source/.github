# Contributing to Claude Customization

This is your personal customization repository! Here's how to organize and extend it effectively.

## Project Structure

```
claude-customization/
├── tools/                 # Custom tools and utilities
│   ├── custom/           # Your personal tools
│   ├── examples/         # Example implementations
│   └── templates/        # Tool templates
├── plugins/              # Custom plugins
├── extensions/           # Browser/IDE extensions
├── agents/               # Agent configurations
├── mcp-servers/          # MCP server implementations
├── config/               # Configuration files
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Adding Custom Tools

### 1. Create Tool File

Copy the template:

```bash
cp tools/templates/javascript-tool.template.js tools/custom/my-tool.js
```

### 2. Implement Tool Logic

Edit `tools/custom/my-tool.js`:

```javascript
module.exports = {
  name: "my-tool",
  description: "What my tool does",
  parameters: {
    type: "object",
    properties: {
      input: { type: "string", description: "Input parameter" }
    },
    required: ["input"]
  },
  execute: async (params) => {
    // Implementation here
    return { success: true, result: "..." };
  }
};
```

### 3. Register Tool

Add to `config/tools.config.json`:

```json
{
  "tools": [
    {
      "name": "my-tool",
      "path": "./tools/custom/my-tool.js",
      "enabled": true
    }
  ]
}
```

### 4. Test Tool

Use Claude to test your tool:

```
I have a tool called "my-tool". Can you test it with input "test-value"?
```

## Adding Plugins

1. Create plugin in `plugins/my-plugin/index.js`
2. Add plugin metadata in `plugins/my-plugin/manifest.json`
3. Register in `config/claude.config.json`

## Adding Custom Agents

1. Create agent config in `agents/my-agent.json`
2. Define tools, system prompt, and settings
3. Test with: `claude-code agent run agents/my-agent.json`

## Code Standards

### Style Guide

- Use 2-space indentation
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

### Error Handling

Always handle errors gracefully:

```javascript
try {
  // Implementation
  return { success: true, data: result };
} catch (error) {
  return { success: false, error: error.message };
}
```

### Documentation

Document your tools:

```javascript
/**
 * Brief description
 * @param {object} params - Tool parameters
 * @returns {object} Result object
 */
```

## Testing

### Unit Tests

Create tests in `tests/my-tool.test.js`:

```javascript
test("my-tool works correctly", async () => {
  const result = await myTool.execute({ input: "test" });
  expect(result.success).toBe(true);
});
```

Run tests:

```bash
npm test
```

### Manual Testing

Test with Claude directly:

```
Test my custom tool with various inputs and tell me if it works correctly.
```

## Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature (tool, plugin, extension)
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions
- `config`: Configuration changes

### Examples

```
feat: add code-analyzer custom tool

Implements analysis of code metrics including complexity,
coverage, and security issues.

Closes #123
```

```
fix: handle errors in file-processor tool

Properly catch and return file processing errors.
```

## Naming Conventions

### Tools

- Use kebab-case: `my-tool`, `code-analyzer`, `file-processor`
- Be descriptive: `git-flow-helper` not `ghf`

### Functions

- Use camelCase: `analyzeFile`, `processData`
- Start with verb: `get`, `set`, `process`, `validate`

### Files

- Use kebab-case for tools: `code-analyzer.js`
- Use PascalCase for classes: `MyAgent.js`
- Use lowercase for configs: `config.json`

## Performance Tips

1. **Avoid redundant operations**: Cache results when possible
2. **Use streaming**: For large file operations
3. **Parallel execution**: Run independent operations concurrently
4. **Optimize patterns**: Use specific glob/grep patterns
5. **Handle timeouts**: Set appropriate timeouts for operations

## Security Considerations

1. **Never commit secrets**: Use `.env` for sensitive data
2. **Validate inputs**: Always validate user inputs
3. **Sanitize output**: Be careful with user-provided data
4. **Use environment variables**: For API keys and credentials
5. **Review permissions**: Check file and directory permissions

## Getting Help

- Check [SETUP.md](./SETUP.md) for setup help
- Review [TOOLS.md](./docs/TOOLS.md) for tool reference
- See [OPTIMIZATION.md](./docs/OPTIMIZATION.md) for performance tips
- Look at examples in `tools/examples/`

## Best Practices

1. **Start with examples**: Copy and modify existing tools
2. **Test thoroughly**: Test with various inputs
3. **Document your code**: Add comments and docstrings
4. **Keep it simple**: Avoid over-engineering
5. **Use git**: Commit frequently with clear messages
6. **Review regularly**: Check for unused code
7. **Update documentation**: Keep docs in sync with code

## Performance Benchmarks

Aim for:

- Tool execution: < 1 second
- File operations: < 100ms per file
- API calls: < 5 seconds with retries
- Parse operations: Linear with input size

## Troubleshooting

### Tool not appearing

- Check `config/tools.config.json` for correct path
- Verify file syntax is valid
- Check console for loading errors

### Tool execution fails

- Check parameter validation
- Review error handling
- Add debug logging
- Test with simple inputs first

### Performance issues

- Use profiling: `console.time()` / `console.timeEnd()`
- Check for blocking operations
- Optimize loops and searches
- Use parallel execution

## Contributing Workflow

1. Create feature branch: `git checkout -b feature/my-tool`
2. Implement and test your feature
3. Commit with clear messages
4. Test thoroughly before finalizing
5. Document your additions
6. Keep commits focused and atomic

## Resources

- [Claude Documentation](https://docs.anthropic.com)
- [Node.js Documentation](https://nodejs.org/docs)
- [JavaScript Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Tool Development Guide](./docs/CUSTOM_TOOLS.md)
- [Optimization Guide](./docs/OPTIMIZATION.md)

---

Happy developing! 🚀
