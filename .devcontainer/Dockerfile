# Optional custom Dockerfile for additional development tools
# This is used if you need more customization beyond the base image

FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install additional development tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    curl \
    wget \
    vim \
    nano \
    htop \
    tmux \
    jq \
    ripgrep \
    fd-find \
    bat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code@latest

# Create workspace directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Set up shell aliases for common Claude operations
RUN echo 'alias cc="npx @anthropic-ai/claude-code"' >> /home/vscode/.bashrc \
    && echo 'alias cc="npx @anthropic-ai/claude-code"' >> /home/vscode/.zshrc

# Configure git
RUN git config --global init.defaultBranch main \
    && git config --global pull.rebase false
