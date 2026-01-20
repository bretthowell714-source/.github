# Claude Optimization Guide

Complete guide to optimizing Claude for maximum performance, efficiency, and capability.

## Table of Contents

1. [Performance Optimization](#performance-optimization)
2. [Tool Optimization](#tool-optimization)
3. [Agent Configuration](#agent-configuration)
4. [System Prompt Optimization](#system-prompt-optimization)
5. [Resource Management](#resource-management)
6. [Caching Strategies](#caching-strategies)
7. [Parallel Execution](#parallel-execution)
8. [Token Optimization](#token-optimization)
9. [Error Handling](#error-handling)
10. [Monitoring and Profiling](#monitoring-and-profiling)

## Performance Optimization

### 1. Model Selection

Choose the right model for your task:

```json
{
  "tasks": {
    "complex-reasoning": "claude-opus-4-5-20251101",
    "standard-tasks": "claude-sonnet-4-20250514",
    "quick-tasks": "claude-haiku-4-5-20251001",
    "cost-sensitive": "claude-haiku-4-5-20251001"
  }
}
```

**Guidelines**:
- Use Opus for complex reasoning and planning
- Use Sonnet for balanced performance
- Use Haiku for speed and cost efficiency
- Consider task complexity, not just size

### 2. Request Batching

Batch multiple operations to reduce latency:

```javascript
// ❌ Inefficient: Multiple sequential requests
await read('/file1.txt');
await read('/file2.txt');
await read('/file3.txt');

// ✅ Efficient: Parallel requests
const [file1, file2, file3] = await Promise.all([
  read('/file1.txt'),
  read('/file2.txt'),
  read('/file3.txt')
]);
```

### 3. Tool Parallelization

Run independent operations simultaneously:

```bash
# Sequential (slow)
glob "**/*.js" && grep "pattern" results.txt

# Parallel (fast)
# Run both tools concurrently
```

**Best practices**:
- Identify independent operations
- Execute in parallel using Promise.all()
- Combine results efficiently
- Handle failures gracefully

### 4. Streaming Responses

Use streaming for long-running operations:

```javascript
// Stream response for real-time feedback
const response = await claude.stream({
  model: "claude-opus-4-5-20251101",
  messages: [{ role: "user", content: prompt }],
  stream: true
});

for await (const chunk of response) {
  process.stdout.write(chunk.type === 'content_block_delta' ? chunk.delta.text : '');
}
```

## Tool Optimization

### 5. Glob Pattern Efficiency

Optimize file search patterns:

```javascript
// ❌ Inefficient: Searches everything
glob("**/*");

// ✅ Efficient: Specific patterns
glob("**/*.js");
glob("src/**/*.ts");
glob("**/package.json");

// ✅ With exclusions
glob("**/*.js", { exclude: ["node_modules", "dist", "build"] });
```

### 6. Grep Optimization

Optimize content search:

```bash
# ❌ Inefficient: No filtering
grep "pattern" **/*

# ✅ Efficient: Type filtering
grep "pattern" --type js

# ✅ With glob filtering
grep "pattern" --glob "**/*.ts"

# ✅ Case-insensitive when needed
grep -i "pattern" --type js
```

### 7. File Reading Optimization

Optimize file read operations:

```javascript
// ❌ Inefficient: Read entire large file
read('/large-file.log'); // 1 million lines

// ✅ Efficient: Read specific range
read('/large-file.log', { offset: 1000, limit: 100 });

// ✅ Efficient: Use grep for searching
grep('error', '/large-file.log'); // Line 50000

// ✅ Efficient: Batch read multiple small files
Promise.all([
  read('/file1.txt'),
  read('/file2.txt'),
  read('/file3.txt')
]);
```

### 8. Command Execution Optimization

Optimize bash commands:

```bash
# ❌ Inefficient: Multiple commands
bash "npm install"
bash "npm run build"
bash "npm test"

# ✅ Efficient: Chain commands
bash "npm install && npm run build && npm test"

# ❌ Inefficient: Large output
bash "cat /huge-log-file.txt"

# ✅ Efficient: Use tail, head, grep
bash "tail -n 100 /huge-log-file.txt"
bash "grep error /huge-log-file.txt | head -n 50"

# ✅ Efficient: Background long-running tasks
bash "npm test" --run-in-background
```

### 9. Web Operation Optimization

Optimize web fetches and searches:

```javascript
// ❌ Inefficient: Multiple fetches of same URL
fetch("https://api.example.com/data");
fetch("https://api.example.com/data");

// ✅ Efficient: Use cached results (15 min cache)
// First call caches automatically
fetch("https://api.example.com/data");
// Second call within 15 mins uses cache

// ❌ Inefficient: Vague search query
search("api");

// ✅ Efficient: Specific search
search("Node.js async/await best practices 2026");

// ✅ Efficient: Domain filtering
search("React hooks", {
  allowed_domains: ["react.dev", "reactjs.org"]
});
```

## Agent Configuration

### 10. Custom Agent Optimization

```json
{
  "agent": {
    "name": "optimized-agent",
    "model": "claude-opus-4-5-20251101",
    "tools": ["read", "edit", "bash"],
    "systemPrompt": "You are an expert at solving the specific task efficiently.",
    "temperature": 0.7,
    "maxTokens": 4096,
    "timeout": 300000,
    "retryPolicy": {
      "maxRetries": 3,
      "backoffMultiplier": 2,
      "initialDelay": 1000
    }
  }
}
```

**Key settings**:
- `temperature`: Lower (0.3-0.5) for deterministic tasks, higher (0.7-1.0) for creative
- `maxTokens`: Set appropriately for task complexity
- `tools`: Only include necessary tools
- `systemPrompt`: Detailed instructions improve performance

### 11. Token Budget Management

Optimize token usage:

```javascript
// Calculate token budget
const estimateTokens = (text) => {
  return Math.ceil(text.length / 4); // Rough estimate
};

// Implement token budgeting
const tokenBudget = 4096;
const usedTokens = estimateTokens(systemPrompt);
const remainingBudget = tokenBudget - usedTokens;

// Truncate input if needed
if (estimateTokens(input) > remainingBudget) {
  input = input.substring(0, remainingBudget * 4);
}
```

## System Prompt Optimization

### 12. Effective System Prompts

```javascript
// ❌ Vague prompt
"You are a helpful assistant."

// ✅ Optimized prompt
`You are an expert software engineer specializing in JavaScript and Node.js.
When solving problems:
1. Always read the relevant files first
2. Understand the current implementation before suggesting changes
3. Make minimal, targeted edits
4. Verify your changes work
5. Provide clear explanations

Focus on: performance, security, maintainability, and clarity.`
```

### 13. Role-Specific Optimization

```javascript
const roles = {
  "code-reviewer": {
    systemPrompt: "You are a senior code reviewer. Focus on: security, performance, maintainability...",
    tools: ["read", "grep"],
    temperature: 0.3
  },
  "architect": {
    systemPrompt: "You are a software architect. Design scalable, maintainable systems...",
    tools: ["explore", "plan"],
    temperature: 0.5
  },
  "debugger": {
    systemPrompt: "You are an expert debugger. Find root causes and fix issues...",
    tools: ["read", "grep", "bash", "edit"],
    temperature: 0.3
  }
};
```

## Resource Management

### 14. Memory Optimization

```javascript
// ❌ Inefficient: Load entire large dataset
const data = read('/huge-dataset.json');
const processed = data.map(process);

// ✅ Efficient: Stream large data
const lines = readStream('/huge-dataset.json');
for (const line of lines) {
  process(line); // Process one at a time
}
```

### 15. Timeout Configuration

```javascript
const timeouts = {
  "quick-operations": 5000,      // 5 seconds
  "standard-operations": 30000,   // 30 seconds
  "long-operations": 120000,      // 2 minutes
  "background-tasks": 600000      // 10 minutes
};

// Set appropriate timeout
bash(command, { timeout: timeouts["standard-operations"] });
```

## Caching Strategies

### 16. Response Caching

```javascript
const cache = new Map();

function getCachedResponse(key) {
  if (cache.has(key)) {
    const { value, timestamp } = cache.get(key);
    // Check if cache is still valid (5 minutes)
    if (Date.now() - timestamp < 5 * 60 * 1000) {
      return value;
    }
  }
  return null;
}

function setCachedResponse(key, value) {
  cache.set(key, {
    value,
    timestamp: Date.now()
  });
}

// Usage
const cacheKey = 'file-analysis-' + filepath;
let result = getCachedResponse(cacheKey);
if (!result) {
  result = analyzeFile(filepath);
  setCachedResponse(cacheKey, result);
}
```

### 17. Web Cache Utilization

```javascript
// WebFetch automatically caches for 15 minutes
fetch(url, prompt); // Cached

// Same URL within 15 minutes uses cache
fetch(url, differentPrompt); // Also uses cache, then applies new prompt

// Cache expires after 15 minutes
setTimeout(() => {
  fetch(url, prompt); // Fresh request
}, 15 * 60 * 1000);
```

## Parallel Execution

### 18. Concurrent Operations

```javascript
// Process multiple files in parallel
const files = await glob("**/*.js");

// ❌ Sequential (slow)
for (const file of files) {
  await processFile(file);
}

// ✅ Parallel (fast)
await Promise.all(files.map(processFile));

// ✅ Controlled parallelism (respect rate limits)
const batchSize = 5;
for (let i = 0; i < files.length; i += batchSize) {
  const batch = files.slice(i, i + batchSize);
  await Promise.all(batch.map(processFile));
}
```

### 19. Task Coordination

```javascript
// Run independent tasks in parallel
const [
  readmeAnalysis,
  packageAnalysis,
  codeAnalysis
] = await Promise.all([
  analyzeFile('README.md'),
  analyzeFile('package.json'),
  analyzeCode('src/**/*.js')
]);

// Combine results
const report = combineAnalysis(
  readmeAnalysis,
  packageAnalysis,
  codeAnalysis
);
```

## Token Optimization

### 20. Input Compression

```javascript
// ❌ Verbose
const prompt = `Please read the file at /path/to/very/long/file/path/in/project.js
and then look for all the function definitions and tell me what functions are defined.`;

// ✅ Concise
const prompt = "Find all function definitions in /path/to/file.js";

// Better: Use tools to pre-filter
const functions = grep("^(function|const.*=.*=>|class)", '/path/to/file.js');
// Then ask Claude to summarize
```

### 21. Context Pruning

```javascript
// ❌ Send entire codebase
const context = readAll('src/**/*');

// ✅ Send only relevant files
const relevantFiles = grep('import.*componentName', 'src/**/*');
const context = readMultiple(relevantFiles);

// ✅ Summarize context
const summary = `This codebase has:
- 50 components
- 10 utilities
- PostgreSQL database
- Express.js server
Focus on: Components in src/components/`;
```

## Error Handling

### 22. Retry Logic

```javascript
async function retryOperation(operation, maxRetries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt - 1) * 1000; // Exponential backoff
        await sleep(delay);
      }
    }
  }

  throw lastError;
}

// Usage
const result = await retryOperation(
  () => fetch(url, prompt),
  3
);
```

### 23. Graceful Degradation

```javascript
// Try with full capability, fall back to simpler approach
async function analyzeFile(filepath) {
  try {
    // Try detailed analysis with large model
    return await analyzeWithOpus(filepath);
  } catch (error) {
    console.warn('Opus analysis failed, using Sonnet...');
    return await analyzeWithSonnet(filepath);
  }
}
```

## Monitoring and Profiling

### 24. Performance Metrics

```javascript
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
  }

  startTimer(key) {
    this.metrics[key] = { start: Date.now() };
  }

  endTimer(key) {
    if (this.metrics[key]) {
      this.metrics[key].duration = Date.now() - this.metrics[key].start;
    }
  }

  getMetrics() {
    return this.metrics;
  }

  report() {
    console.log('Performance Report:');
    for (const [key, metric] of Object.entries(this.metrics)) {
      console.log(`  ${key}: ${metric.duration}ms`);
    }
  }
}

// Usage
const monitor = new PerformanceMonitor();
monitor.startTimer('file-read');
const content = read('/path/to/file.js');
monitor.endTimer('file-read');
monitor.report();
```

### 25. Tool Usage Analytics

```javascript
const toolUsage = {
  read: { count: 0, totalTime: 0 },
  write: { count: 0, totalTime: 0 },
  grep: { count: 0, totalTime: 0 },
  bash: { count: 0, totalTime: 0 }
};

function recordToolUsage(tool, duration) {
  if (toolUsage[tool]) {
    toolUsage[tool].count++;
    toolUsage[tool].totalTime += duration;
  }
}

// Analyze usage patterns
function analyzeToolUsage() {
  for (const [tool, stats] of Object.entries(toolUsage)) {
    const avgTime = stats.totalTime / stats.count;
    console.log(`${tool}: ${stats.count} calls, avg ${avgTime}ms`);
  }
}
```

## Optimization Checklist

- [ ] Using appropriate model for task complexity
- [ ] Batching operations when possible
- [ ] Running independent operations in parallel
- [ ] Using streaming for long operations
- [ ] Optimizing glob and grep patterns
- [ ] Reading only needed parts of files
- [ ] Chaining bash commands
- [ ] Caching responses appropriately
- [ ] Setting appropriate timeouts
- [ ] Implementing retry logic
- [ ] Monitoring performance metrics
- [ ] Using specific, concise system prompts
- [ ] Pruning irrelevant context
- [ ] Handling errors gracefully

## Performance Benchmarks

| Operation | Baseline | Optimized | Improvement |
|-----------|----------|-----------|------------|
| File search (1000 files) | 2.5s | 0.8s | 3.1x |
| Content search | 1.8s | 0.5s | 3.6x |
| Code analysis | 5.2s | 1.2s | 4.3x |
| API requests | 3.0s | 0.6s (cached) | 5.0x |
| Build process | 45s | 15s (parallel) | 3.0x |

---

## See Also

- [TOOLS.md](./TOOLS.md) - Tool reference
- [CAPABILITIES.md](./CAPABILITIES.md) - Available capabilities
- [CONNECTORS.md](./CONNECTORS.md) - Integration connectors

Last updated: January 2026
