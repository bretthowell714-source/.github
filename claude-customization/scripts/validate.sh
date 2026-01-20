#!/bin/bash

# Validation script for Claude Customization Workspace

echo "Validating Claude Customization setup..."
echo ""

validation_passed=true

# Check directories
echo "Checking directory structure..."
dirs=(
    "tools/custom"
    "tools/examples"
    "tools/templates"
    "plugins"
    "extensions"
    "agents"
    "mcp-servers"
    "config"
    "docs"
    "scripts"
    "logs"
)

for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ Missing: $dir"
        validation_passed=false
    fi
done

# Check files
echo ""
echo "Checking configuration files..."
files=(
    "README.md"
    ".env"
    ".env.example"
    ".gitignore"
    "package.json"
    "config/claude.config.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ Missing: $file"
        if [[ "$file" != ".env" ]]; then
            validation_passed=false
        fi
    fi
done

# Check API key
echo ""
echo "Checking API configuration..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
        echo "  ✓ ANTHROPIC_API_KEY configured"
    else
        echo "  ⚠ ANTHROPIC_API_KEY not set (required for API usage)"
    fi
else
    echo "  ✓ ANTHROPIC_API_KEY set"
fi

# Check Node.js modules
echo ""
echo "Checking Node.js installation..."
if [ -d "node_modules" ]; then
    echo "  ✓ node_modules exists"
else
    echo "  ⚠ node_modules not installed (run: npm install)"
fi

# Summary
echo ""
echo "================================"
if [ "$validation_passed" = true ]; then
    echo "✓ Validation passed!"
    echo "================================"
    exit 0
else
    echo "⚠ Some issues found (see above)"
    echo "================================"
    echo ""
    echo "To fix issues:"
    echo "1. Run setup script: bash scripts/setup.sh"
    echo "2. Create missing directories: mkdir -p [directory]"
    echo "3. Copy missing files from templates"
    exit 1
fi
