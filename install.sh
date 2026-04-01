#!/usr/bin/env bash

set -e

REPO_URL="git+https://github.com/bartekmarczyk6/exa-cli.git"
CLI_NAME="exa-cli"

echo "🚀 Installing $CLI_NAME..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3.9 or higher and try again."
    exit 1
fi

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo "📦 pipx is not installed. Installing pipx..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    
    # Export path for the current session so the next command works
    export PATH="$PATH:$HOME/.local/bin"
    
    echo "✅ pipx installed successfully. You may need to restart your terminal or run 'source ~/.bashrc' (or equivalent) after this script finishes to use pipx globally."
fi

# Install the CLI using pipx directly from GitHub
echo "📥 Downloading and installing $CLI_NAME from GitHub..."
pipx install "$REPO_URL" --force

echo ""
echo "✨ Installation Complete! ✨"
echo "You can now use the CLI by typing 'exa' in your terminal."
echo ""
echo "Next steps:"
echo "  1. Set your API key: export EXA_API_KEY=\"your-api-key\""
echo "  2. Run a search: exa search \"latest breakthroughs in AI\""
