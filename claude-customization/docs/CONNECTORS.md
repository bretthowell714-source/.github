# Claude Connectors & Integrations

Complete guide to connecting Claude with external systems, APIs, services, and databases.

## Table of Contents

1. [API Connectors](#api-connectors)
2. [VCS Connectors](#vcs-connectors)
3. [Database Connectors](#database-connectors)
4. [Service Integrations](#service-integrations)
5. [MCP Servers](#mcp-servers)
6. [Webhook Connectors](#webhook-connectors)
7. [Cloud Platform Integration](#cloud-platform-integration)
8. [IDE & Editor Integration](#ide--editor-integration)
9. [Authentication & Security](#authentication--security)
10. [Custom Connector Development](#custom-connector-development)

## API Connectors

### 1. REST API Integration

**Built-in Tool**: WebFetch

```javascript
// Fetch JSON API
const data = await fetch('https://api.example.com/data', 'Extract the user list');

// POST request with custom headers
const response = await bash(`curl -X POST https://api.example.com/endpoint \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${process.env.API_TOKEN}" \
  -d '{"key": "value"}'`);
```

**Configuration**:

```json
{
  "api-connectors": {
    "rest": {
      "enabled": true,
      "timeout": 30000,
      "retries": 3,
      "headers": {
        "User-Agent": "Claude-Customization/1.0"
      }
    }
  }
}
```

### 2. GraphQL Integration

```javascript
// GraphQL query via REST API
const query = `
  query GetUser($id: ID!) {
    user(id: $id) {
      name
      email
      posts {
        title
      }
    }
  }
`;

const response = await bash(`curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "${query}", "variables": {"id": "123"}}'`);
```

### 3. OpenAPI/Swagger Integration

```javascript
// Load OpenAPI spec
const spec = read('/path/to/openapi.json');

// Parse and generate tools from spec
const tools = parseOpenAPI(JSON.parse(spec));

// Configuration
```json
{
  "openapi-connector": {
    "spec-path": "./openapi.json",
    "auto-generate-tools": true,
    "base-url": "https://api.example.com"
  }
}
```

## VCS Connectors

### 4. GitHub Integration

**Built-in**: GitHub CLI (gh)

```bash
# Clone repository
bash "git clone https://github.com/user/repo.git"

# Create pull request
bash "gh pr create --title 'Feature' --body 'Description'"

# Check PR status
bash "gh pr status"

# Merge pull request
bash "gh pr merge"

# Create issue
bash "gh issue create --title 'Bug' --body 'Bug description'"
```

**Configuration**:

```bash
# Setup GitHub CLI
gh auth login
gh auth set-host github.com --with-token < token.txt

# Configure in .env
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

### 5. GitLab Integration

```bash
# Clone GitLab repository
bash "git clone https://gitlab.com/user/repo.git"

# Use git operations (same as GitHub)
bash "git push origin main"

# API calls via curl
bash "curl --header 'PRIVATE-TOKEN: ${GITLAB_TOKEN}' \
  https://gitlab.com/api/v4/projects"
```

### 6. Bitbucket Integration

```bash
# Clone Bitbucket repository
bash "git clone https://bitbucket.org/user/repo.git"

# Use Bitbucket CLI
bash "bb pr list"
bash "bb pr create --title 'Feature'"
```

## Database Connectors

### 7. PostgreSQL

```javascript
// Via connection string
const connString = `postgresql://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_HOST}:5432/${process.env.DB_NAME}`;

// Query via Node.js client
const response = await bash(`psql ${connString} -c "SELECT * FROM users;"`);

// Via Docker
bash "docker exec db psql -U user -d database -c 'SELECT * FROM table;'";
```

**Configuration**:

```env
DB_USER=postgres
DB_PASS=password
DB_HOST=localhost
DB_NAME=mydb
DB_PORT=5432
```

### 8. MongoDB

```javascript
// Connection string
const mongoUri = `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@cluster.mongodb.net/${process.env.MONGO_DB}`;

// Query via mongosh
bash `mongosh "${mongoUri}" --eval "db.collection.find().limit(10).pretty()"`;
```

### 9. MySQL/MariaDB

```bash
# Connect and query
bash "mysql -h ${DB_HOST} -u ${DB_USER} -p${DB_PASS} ${DB_NAME} -e 'SELECT * FROM users;'"
```

### 10. Redis

```bash
# Connect to Redis
bash "redis-cli -h ${REDIS_HOST} -p ${REDIS_PORT} PING"

# Get value
bash "redis-cli GET mykey"

# Set value
bash "redis-cli SET mykey 'value'"
```

## Service Integrations

### 11. Docker Integration

```bash
# List containers
bash "docker ps"

# Run command in container
bash "docker exec container-name ls -la"

# Execute script in container
bash "docker exec container-name bash /path/to/script.sh"

# Build image
bash "docker build -t myimage:latest ."
```

### 12. Kubernetes Integration

```bash
# List pods
bash "kubectl get pods"

# Get pod logs
bash "kubectl logs pod-name -f"

# Execute command in pod
bash "kubectl exec pod-name -- bash /path/to/script.sh"

# Deploy application
bash "kubectl apply -f deployment.yaml"
```

### 13. AWS Integration

```bash
# Configure AWS CLI
bash "aws configure set aws_access_key_id ${AWS_ACCESS_KEY}"
bash "aws configure set aws_secret_access_key ${AWS_SECRET_KEY}"

# List S3 buckets
bash "aws s3 ls"

# Deploy Lambda
bash "aws lambda update-function-code --function-name myfunction --zip-file fileb://function.zip"

# Deploy CloudFormation
bash "aws cloudformation deploy --template-file template.yaml --stack-name mystack"
```

### 14. Google Cloud Integration

```bash
# Authenticate
bash "gcloud auth login"

# List resources
bash "gcloud compute instances list"

# Deploy application
bash "gcloud app deploy"

# Deploy Cloud Function
bash "gcloud functions deploy myfunction --entry-point handler --runtime nodejs18"
```

### 15. Azure Integration

```bash
# Login to Azure
bash "az login"

# List resources
bash "az resource list"

# Deploy template
bash "az deployment group create --resource-group mygroup --template-file template.json"
```

## MCP Servers

### 16. MCP Server Connector

**Purpose**: Connect to Model Context Protocol servers for extended capabilities

```json
{
  "mcp-servers": [
    {
      "name": "filesystem-server",
      "uri": "stdio:///path/to/server",
      "env": {}
    },
    {
      "name": "custom-api-server",
      "uri": "http://localhost:8000",
      "auth": {
        "token": "${CUSTOM_SERVER_TOKEN}"
      }
    }
  ]
}
```

### 17. Custom MCP Server Implementation

```javascript
// mcp-servers/my-server.js
const MCPServer = require("@anthropic-ai/mcp-server");

const server = new MCPServer({
  name: "my-mcp-server",
  version: "1.0.0",
  capabilities: {
    tools: {}
  }
});

// Define tools
server.tool("list-resources", {
  description: "List all available resources",
  inputSchema: {
    type: "object",
    properties: {
      filter: {
        type: "string",
        description: "Filter pattern"
      }
    }
  }
}, async (input) => {
  // Implementation
  return { resources: [] };
});

// Define resources
server.resource("resource://data/users", async () => {
  return { content: getUsers() };
});

server.start();
```

## Webhook Connectors

### 18. Incoming Webhooks

```javascript
// Receive webhook from external service
const express = require('express');
const app = express();

app.post('/webhook', (req, res) => {
  const event = req.body;

  // Process webhook
  if (event.type === 'deployment.completed') {
    triggerAnalysis(event.data);
  }

  res.json({ status: 'received' });
});

app.listen(3000);
```

### 19. Outgoing Webhooks

```bash
# Send notification via webhook
bash "curl -X POST https://hooks.example.com/notify \
  -H 'Content-Type: application/json' \
  -d '{
    \"event\": \"analysis_complete\",
    \"status\": \"success\",
    \"timestamp\": \"2026-01-20T10:00:00Z\"
  }'"
```

## Cloud Platform Integration

### 20. Vercel Integration

```bash
# Deploy to Vercel
bash "vercel --prod"

# View deployment logs
bash "vercel logs"

# Configure environment
bash "vercel env add NEXT_PUBLIC_API_URL"
```

### 21. Heroku Integration

```bash
# Login to Heroku
bash "heroku login"

# Deploy application
bash "git push heroku main"

# View logs
bash "heroku logs -t"
```

### 22. Digital Ocean Integration

```bash
# Configure doctl
bash "doctl auth init --access-token ${DIGITAL_OCEAN_TOKEN}"

# List apps
bash "doctl apps list"

# Deploy app
bash "doctl apps create --spec app.yaml"
```

## IDE & Editor Integration

### 23. Claude Code CLI

```bash
# Configure workspace
claude-code config set workspace $(pwd)

# Enable custom tools
claude-code config set customToolsPath ./tools

# Run with custom settings
claude-code task "analyze code" \
  --model claude-opus-4-5-20251101 \
  --tools read,grep,bash
```

### 24. VS Code Extension

```json
{
  "claude.apiKey": "${ANTHROPIC_API_KEY}",
  "claude.model": "claude-opus-4-5-20251101",
  "claude.customTools": "./tools/custom",
  "claude.autoSave": true
}
```

### 25. JetBrains IDE Integration

Configure in IDE settings:

```
Editor → Claude Settings:
- API Key: ANTHROPIC_API_KEY
- Model: claude-opus-4-5-20251101
- Enable inline suggestions: true
- Custom tools path: ./tools/custom
```

## Authentication & Security

### 26. API Key Management

```bash
# Store in .env (not in git)
ANTHROPIC_API_KEY=sk-xxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@host/db

# Load in code
require('dotenv').config();
const apiKey = process.env.ANTHROPIC_API_KEY;
```

### 27. OAuth 2.0 Integration

```javascript
// OAuth callback handler
app.get('/callback', async (req, res) => {
  const code = req.query.code;

  // Exchange code for token
  const token = await exchangeCodeForToken(code);

  // Store token securely
  storeToken(token);

  res.redirect('/dashboard');
});

// Use token for API calls
const headers = {
  'Authorization': `Bearer ${token}`
};
```

### 28. Secrets Management

```bash
# Use environment variables
export SECRET_KEY=$(openssl rand -hex 32)

# Or use secrets manager
bash "aws secretsmanager get-secret-value --secret-id my-secret"

# Or use HashiCorp Vault
bash "vault read secret/my-secret"
```

## Custom Connector Development

### 29. Creating Custom Connectors

```javascript
// connectors/custom-api-connector.js
class CustomAPIConnector {
  constructor(config) {
    this.baseURL = config.baseURL;
    this.apiKey = config.apiKey;
    this.timeout = config.timeout || 30000;
  }

  async request(method, endpoint, data = null) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    };

    const options = { method, headers, timeout: this.timeout };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);
    return response.json();
  }

  async get(endpoint) {
    return this.request('GET', endpoint);
  }

  async post(endpoint, data) {
    return this.request('POST', endpoint, data);
  }

  async put(endpoint, data) {
    return this.request('PUT', endpoint, data);
  }

  async delete(endpoint) {
    return this.request('DELETE', endpoint);
  }
}

module.exports = CustomAPIConnector;
```

### 30. Connector Registration

```json
{
  "connectors": [
    {
      "name": "custom-api",
      "path": "./connectors/custom-api-connector.js",
      "config": {
        "baseURL": "${CUSTOM_API_URL}",
        "apiKey": "${CUSTOM_API_KEY}",
        "timeout": 30000
      },
      "enabled": true
    }
  ]
}
```

## Integration Patterns

### Pattern 1: Data Pipeline

```
Source (DB) → Process (Claude) → Transform (Script) → Destination (API)
```

### Pattern 2: CI/CD Integration

```
Git Push → GitHub Actions → Claude Analysis → Deployment → Webhook Notification
```

### Pattern 3: Real-time Monitoring

```
Service → Webhook → Claude Processing → Alert System → Notification
```

### Pattern 4: Multi-Source Analysis

```
Database + APIs + Files → Claude Analysis → Report Generation → Storage
```

## Connector Configuration Template

```json
{
  "connector": {
    "name": "my-connector",
    "type": "api|database|service|custom",
    "enabled": true,
    "config": {
      "url": "${CONNECTOR_URL}",
      "auth": {
        "type": "api-key|oauth|basic",
        "credentials": "${CONNECTOR_AUTH}"
      },
      "timeout": 30000,
      "retries": 3
    },
    "tools": [
      {
        "name": "connector-tool-1",
        "description": "Tool description",
        "enabled": true
      }
    ]
  }
}
```

## Common Connector Issues

| Issue | Solution |
|-------|----------|
| Authentication fails | Verify credentials in .env, check API key permissions |
| Connection timeout | Increase timeout value, check network connectivity |
| Rate limiting | Implement backoff strategy, use batch operations |
| SSL/TLS errors | Update certificates, disable verification (dev only) |
| Firewall blocked | Configure firewall rules, use proxy if needed |

---

## See Also

- [OPTIMIZATION.md](./OPTIMIZATION.md) - Performance optimization
- [TOOLS.md](./TOOLS.md) - Tool reference
- [CUSTOM_TOOLS.md](./CUSTOM_TOOLS.md) - Custom tool development

Last updated: January 2026
