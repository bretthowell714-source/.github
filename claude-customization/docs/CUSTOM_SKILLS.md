# Custom Skills Guide

Complete guide to creating, registering, and using custom skills in Claude.

## Table of Contents

1. [What are Custom Skills?](#what-are-custom-skills)
2. [Quick Start](#quick-start)
3. [Creating Skills](#creating-skills)
4. [Skill Structure](#skill-structure)
5. [Registering Skills](#registering-skills)
6. [Examples](#examples)
7. [Best Practices](#best-practices)
8. [Advanced Skills](#advanced-skills)
9. [Troubleshooting](#troubleshooting)

## What are Custom Skills?

Custom skills are capabilities you add to Claude that extend its functionality beyond the built-in tools. They allow you to:

- Create specialized functions for your specific use cases
- Integrate with external services and APIs
- Build domain-specific expertise
- Automate complex workflows
- Add company or project-specific knowledge

### Types of Skills

1. **Simple Skills** - Single-purpose utilities (5-50 lines)
2. **Complex Skills** - Multi-step workflows (50-500 lines)
3. **Integration Skills** - External service connectors
4. **Domain Skills** - Specialized knowledge areas
5. **Composite Skills** - Combine multiple tools

## Quick Start

### 1. Create a Simple Skill

Create `skills/my-first-skill.js`:

```javascript
module.exports = {
  name: "my-first-skill",
  description: "My first Claude skill",
  execute: async (input) => {
    return {
      success: true,
      result: `Processed: ${input}`
    };
  }
};
```

### 2. Register the Skill

Add to `.env`:

```env
CUSTOM_SKILLS_PATH=./skills
```

### 3. Use It

Tell Claude:

```
I have a skill called "my-first-skill".
Use it to process "hello world".
```

## Creating Skills

### Directory Structure

```
skills/
├── simple/              # Simple, single-purpose skills
│   ├── text-formatter.js
│   ├── math-helper.js
│   └── string-utils.js
├── integration/         # External service skills
│   ├── github-helper.js
│   ├── slack-notifier.js
│   └── email-sender.js
├── domain/              # Domain-specific skills
│   ├── code-reviewer.js
│   ├── data-analyst.js
│   └── ml-assistant.js
├── templates/           # Skill templates
│   ├── simple.template.js
│   ├── integration.template.js
│   └── domain.template.js
└── registry.json        # Skill registry
```

## Skill Structure

### Minimal Skill

```javascript
module.exports = {
  name: "skill-name",
  description: "What the skill does",
  execute: async (input) => {
    // Implementation
    return { success: true, result: output };
  }
};
```

### Full-Featured Skill

```javascript
module.exports = {
  // Required
  name: "skill-name",
  description: "Detailed description",
  version: "1.0.0",

  // Optional metadata
  author: "Your Name",
  tags: ["category", "tags"],
  category: "Utility",

  // Input/output specification
  input: {
    type: "string | object | array",
    description: "Input description",
    examples: ["example1", "example2"]
  },

  output: {
    type: "object",
    properties: {
      success: { type: "boolean" },
      result: { type: "string | object" },
      error: { type: "string" }
    }
  },

  // Configuration options
  options: {
    timeout: 30000,
    retries: 3,
    cache: true,
    cacheTTL: 3600000
  },

  // Initialization (optional)
  init: async (config) => {
    // Setup code
  },

  // Main execution
  execute: async (input, context) => {
    // Implementation
  },

  // Cleanup (optional)
  cleanup: async () => {
    // Cleanup code
  },

  // Validation
  validate: (input) => {
    if (!input) throw new Error("Input required");
    return true;
  }
};
```

## Registering Skills

### Method 1: Auto-Registration

Create `skills/registry.json`:

```json
{
  "skills": [
    {
      "name": "my-skill",
      "path": "./simple/my-skill.js",
      "enabled": true,
      "version": "1.0.0"
    },
    {
      "name": "github-helper",
      "path": "./integration/github-helper.js",
      "enabled": true,
      "config": {
        "apiKey": "${GITHUB_TOKEN}"
      }
    }
  ]
}
```

### Method 2: Manual Registration

In `config/claude.config.json`:

```json
{
  "skills": {
    "enabled": true,
    "auto-load": true,
    "path": "./skills",
    "registry": [
      {
        "name": "my-skill",
        "path": "./my-skill.js",
        "enabled": true
      }
    ]
  }
}
```

## Examples

### Example 1: Text Formatting Skill

```javascript
// skills/simple/text-formatter.js
module.exports = {
  name: "text-formatter",
  description: "Format text in various ways",
  execute: async (input) => {
    return {
      success: true,
      original: input,
      uppercase: input.toUpperCase(),
      lowercase: input.toLowerCase(),
      reversed: input.split('').reverse().join(''),
      wordCount: input.split(/\s+/).length,
      charCount: input.length
    };
  }
};
```

**Usage:**
```
Use the "text-formatter" skill to format "hello world"
```

### Example 2: GitHub Integration Skill

```javascript
// skills/integration/github-helper.js
const axios = require('axios');

module.exports = {
  name: "github-helper",
  description: "Interact with GitHub API",
  execute: async (input, context) => {
    const { action, owner, repo, ...params } = input;

    const headers = {
      'Authorization': `token ${process.env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json'
    };

    try {
      let response;

      switch (action) {
        case 'get-repo':
          response = await axios.get(
            `https://api.github.com/repos/${owner}/${repo}`,
            { headers }
          );
          break;

        case 'list-issues':
          response = await axios.get(
            `https://api.github.com/repos/${owner}/${repo}/issues`,
            { headers }
          );
          break;

        case 'create-issue':
          response = await axios.post(
            `https://api.github.com/repos/${owner}/${repo}/issues`,
            { title: params.title, body: params.body },
            { headers }
          );
          break;

        default:
          throw new Error(`Unknown action: ${action}`);
      }

      return {
        success: true,
        action,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};
```

**Usage:**
```
Use the "github-helper" skill to get information about the repo "bretthowell714-source/claude-customization"
```

### Example 3: Domain-Specific Skill (Code Reviewer)

```javascript
// skills/domain/code-reviewer.js
module.exports = {
  name: "code-reviewer",
  description: "Review code for quality and best practices",
  execute: async (code) => {
    const issues = [];

    // Check for common issues
    if (code.includes('eval(')) {
      issues.push({
        severity: 'critical',
        message: 'eval() is unsafe, consider alternatives'
      });
    }

    if (!code.includes('try') && !code.includes('catch')) {
      issues.push({
        severity: 'warning',
        message: 'No error handling found'
      });
    }

    if (code.length > 500) {
      issues.push({
        severity: 'info',
        message: 'Function is long, consider breaking into smaller functions'
      });
    }

    return {
      success: true,
      issuesFound: issues.length,
      issues: issues,
      score: Math.max(0, 100 - issues.length * 20)
    };
  }
};
```

**Usage:**
```
Review this code using the "code-reviewer" skill:
[paste code]
```

## Best Practices

### 1. Naming Conventions

```javascript
// ✓ Good
"email-sender"
"github-api-helper"
"code-analyzer"

// ✗ Bad
"ES"
"helper"
"tool1"
```

### 2. Error Handling

```javascript
// ✓ Good
execute: async (input) => {
  try {
    const result = await process(input);
    return { success: true, result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ✗ Bad
execute: async (input) => {
  return { result: await process(input) };
}
```

### 3. Input Validation

```javascript
// ✓ Good
validate: (input) => {
  if (typeof input !== 'string') {
    throw new Error('Input must be string');
  }
  if (input.length === 0) {
    throw new Error('Input cannot be empty');
  }
  return true;
},

// ✗ Bad
execute: async (input) => {
  // No validation
}
```

### 4. Documentation

```javascript
/**
 * Format text in various ways
 *
 * @param {string} input - Text to format
 * @returns {object} Object with formatted variations
 *
 * @example
 * execute("hello world")
 * // Returns: { uppercase: "HELLO WORLD", ... }
 */
execute: async (input) => {
  // ...
}
```

### 5. Performance

```javascript
// ✓ Good - Use caching
const cache = new Map();
execute: async (input) => {
  if (cache.has(input)) return cache.get(input);
  const result = await expensiveOperation(input);
  cache.set(input, result);
  return result;
}

// ✗ Bad - No caching
execute: async (input) => {
  return await expensiveOperation(input);
}
```

## Advanced Skills

### 1. Async/Await Skill

```javascript
module.exports = {
  name: "async-processor",
  description: "Process data asynchronously",
  execute: async (items) => {
    const results = await Promise.all(
      items.map(async (item) => {
        return await processItem(item);
      })
    );
    return { success: true, results };
  }
};
```

### 2. Stateful Skill

```javascript
module.exports = {
  name: "stateful-skill",
  description: "Skill with internal state",
  state: {},

  init: async (config) => {
    this.state = { counter: 0, history: [] };
  },

  execute: async (input) => {
    this.state.counter++;
    this.state.history.push(input);

    return {
      success: true,
      counter: this.state.counter,
      history: this.state.history
    };
  }
};
```

### 3. Skill with Dependencies

```javascript
module.exports = {
  name: "api-skill",
  description: "Skill using external APIs",
  dependencies: ['axios', 'dotenv'],

  execute: async (input) => {
    const axios = require('axios');
    const response = await axios.get(`https://api.example.com/data?q=${input}`);
    return { success: true, data: response.data };
  }
};
```

## Troubleshooting

### Skill Not Found

**Problem**: Claude says skill doesn't exist

**Solutions**:
1. Check skill file path in registry
2. Verify file syntax is correct
3. Restart Claude Code
4. Check `CUSTOM_SKILLS_PATH` environment variable

### Execution Errors

**Problem**: Skill executes but returns error

**Solutions**:
1. Add try-catch error handling
2. Validate inputs
3. Check dependencies are installed
4. Review error logs

### Performance Issues

**Problem**: Skill runs slowly

**Solutions**:
1. Add caching
2. Optimize algorithms
3. Use async/await properly
4. Profile with console.time()

### Integration Issues

**Problem**: External API integration fails

**Solutions**:
1. Check API credentials in `.env`
2. Verify API endpoint is correct
3. Check rate limiting
4. Review API documentation

## Skill Development Workflow

1. **Create** - Write skill file
2. **Test** - Use with Claude
3. **Debug** - Check logs and errors
4. **Optimize** - Add caching, improve performance
5. **Document** - Add comments and examples
6. **Register** - Add to registry
7. **Share** - Commit to repository

## Common Skill Patterns

### Pattern 1: Data Transformer

```javascript
execute: async (input) => {
  const transformed = transform(input);
  return { success: true, result: transformed };
}
```

### Pattern 2: External Service Connector

```javascript
execute: async (params) => {
  const response = await externalAPI.request(params);
  return { success: true, data: response };
}
```

### Pattern 3: Analysis Tool

```javascript
execute: async (data) => {
  const analysis = analyze(data);
  return { success: true, analysis };
}
```

### Pattern 4: Multi-Step Workflow

```javascript
execute: async (input) => {
  const step1 = await doStep1(input);
  const step2 = await doStep2(step1);
  const step3 = await doStep3(step2);
  return { success: true, result: step3 };
}
```

## Resources

- [Tool Development Guide](./CUSTOM_TOOLS.md)
- [Optimization Guide](./OPTIMIZATION.md)
- [API Examples](./CONNECTORS.md)

---

Last updated: January 2026
