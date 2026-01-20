#!/bin/bash

# Setup script for Claude Customization Workspace

echo "================================"
echo "Claude Customization Setup"
echo "================================"

# Check Node.js
echo ""
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✓ Node.js $(node --version) installed"

# Check npm
echo ""
echo "Checking npm installation..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi
echo "✓ npm $(npm --version) installed"

# Setup environment
echo ""
echo "Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (remember to fill in your API keys!)"
else
    echo "✓ .env file already exists"
fi

# Create directories
echo ""
echo "Creating directories..."
mkdir -p tools/custom plugins/custom extensions/custom agents/custom mcp-servers/custom config logs scripts/hooks

echo "✓ Directories created"

# Install dependencies
echo ""
echo "Installing dependencies..."
npm install
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Validate setup
echo ""
echo "Validating setup..."
bash scripts/validate.sh

echo ""
echo "================================"
echo "✓ Setup complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - ANTHROPIC_API_KEY from https://console.anthropic.com"
echo "   - GITHUB_TOKEN from https://github.com/settings/tokens"
echo ""
echo "2. Read documentation:"
echo "   - SETUP.md - Getting started guide"
echo "   - docs/CAPABILITIES.md - Available capabilities"
echo "   - docs/TOOLS.md - Tool reference"
echo ""
echo "3. Explore examples:"
echo "   - tools/examples/ - Example custom tools"
echo "   - agents/examples/ - Example agent configurations"
echo ""
echo "4. Create your first custom tool:"
echo "   cp tools/templates/javascript-tool.template.js tools/custom/my-tool.js"
echo ""
echo "Happy customizing! 🚀"
