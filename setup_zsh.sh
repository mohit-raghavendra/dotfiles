#!/bin/bash
# Install zsh if not already present

set -e

if command -v zsh >/dev/null 2>&1; then
    echo "zsh already installed"
    exit 0
fi

echo "Installing zsh..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    brew install zsh
else
    # Assume Ubuntu/Debian for servers
    sudo apt-get update
    sudo apt-get install -y zsh
fi

echo "zsh installed successfully"
