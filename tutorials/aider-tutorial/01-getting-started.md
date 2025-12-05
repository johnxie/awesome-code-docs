---
layout: default
title: "Aider Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Aider Tutorial
---

# Chapter 1: Getting Started with Aider

> Install Aider, configure your environment, and make your first AI-powered code edits.

## Overview

This chapter guides you through installing Aider, setting up your environment, and making your first AI-powered code changes. By the end, you'll have Aider running and be able to collaborate with AI on your code projects.

## Installation

### Prerequisites

```bash
# Required tools
- Python 3.8 or later
- Git (for repository integration)
- pip or pipx (recommended for isolation)

# Verify versions
python --version  # Should be 3.8+
git --version     # Any recent version
```

### Installing with pipx (Recommended)

```bash
# Install pipx if not already installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install Aider
pipx install aider-chat

# Verify installation
aider --version
```

### Alternative: Installing with pip

```bash
# Install globally (not recommended for production)
pip install aider-chat

# Or in a virtual environment
python -m venv aider-env
source aider-env/bin/activate  # On Windows: aider-env\Scripts\activate
pip install aider-chat
```

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/Aider-AI/aider.git
cd aider

# Install in development mode
pip install -e .

# Verify installation
aider --version
```

## API Key Configuration

### OpenAI API Key

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Test the key
aider --model gpt-4o --dry-run "hello"
```

### Anthropic API Key

```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key-here"

# Test the key
aider --model claude-3-5-sonnet-20241022 --dry-run "hello"
```

### Other Providers

```bash
# Google Gemini
export GEMINI_API_KEY="your-gemini-api-key"

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"

# Local models (via Ollama)
# No API key needed, just install Ollama
```

### Persistent Configuration

```bash
# Create a configuration file
cat > ~/.aider.conf.yml << EOF
model: claude-3-5-sonnet-20241022
auto-commits: true
dark-mode: true
editor: vim  # or code, emacs, etc.
gitignore: true
EOF

# Or set environment variables in your shell profile
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
echo 'export AIDER_DARK_MODE=true' >> ~/.bashrc
```

## Your First Aider Session

### Starting Aider

```bash
# Navigate to a git repository
cd my-project

# Start Aider with default model
aider

# Start with specific model
aider --model claude-3-5-sonnet-20241022

# Start with voice support
aider --voice

# Start in architect mode
aider --architect
```

### Understanding the Interface

```bash
$ aider --model gpt-4o

Aider v0.50.0
Models: gpt-4o with diff edit format
Git repo: .git with 12 files
Repo-map: using 1024 tokens

>
```

**Interface Components:**
- **Version Info**: Shows Aider version and model
- **Git Status**: Indicates repository and file count
- **Token Usage**: Shows repo-map token allocation
- **Prompt**: Ready for your input

### Your First Code Change

Let's start with a simple Python project:

```bash
# Create a sample project
mkdir hello-aider
cd hello-aider
git init

# Create a simple Python file
cat > hello.py << 'EOF'
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
EOF

# Commit initial version
git add .
git commit -m "Initial hello.py"
```

Now let's use Aider to enhance this code:

```bash
# Start Aider
aider

# Add the file to the conversation
> /add hello.py

# Make a request
> Add a function to calculate the factorial of a number, and modify the main section to use both functions.
```

**Expected Output:**
```
I'll add a factorial function and modify the main section to demonstrate both functions.

hello.py
<<<<<<< SEARCH
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
=======
def greet(name):
    return f"Hello, {name}!"

def factorial(n):
    """Calculate the factorial of a number."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    print(greet("World"))
    print(f"Factorial of 5 is: {factorial(5)}")
>>>>>>> REPLACE
```

**Accept the changes:**
```
> y
```

**Result:**
```
Commit: feat: Add factorial function and demonstrate both functions
```

## Understanding the Workflow

### The Aider Workflow

```mermaid
flowchart TD
    A[Start Aider] --> B[Add Files]
    B --> C[Make Request]
    C --> D[AI Analyzes]
    D --> E[AI Plans Changes]
    E --> F[Show Diff]
    F --> G{Accept?}
    G -->|Yes| H[Apply Changes]
    G -->|No| I[Refine Request]
    I --> C
    H --> J[Git Commit]
    J --> K[Continue or Exit]

    classDef user fill:#e1f5fe,stroke:#01579b
    classDef aider fill:#f3e5f5,stroke:#4a148c

    class A,B,C,G,I,K user
    class D,E,F,H,J aider
```

### Key Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `/add <file>` | Add file to conversation | `/add src/main.py` |
| `/drop <file>` | Remove file from conversation | `/drop old.py` |
| `/ls` | List files in conversation | `/ls` |
| `/diff` | Show pending changes | `/diff` |
| `/undo` | Undo last commit | `/undo` |
| `/clear` | Clear conversation history | `/clear` |
| `/help` | Show all commands | `/help` |

### Managing Files

```bash
# Add multiple files
> /add src/main.py src/utils.py tests/

# Add with wildcards
> /add src/**/*.py

# Check what's in the conversation
> /ls

# Files in chat:
# src/main.py
# src/utils.py
# tests/test_main.py

# Remove a file
> /drop src/utils.py
```

## Working with Different Models

### Model Selection

```bash
# OpenAI models
aider --model gpt-4o              # Latest GPT-4o
aider --model gpt-4-turbo         # Fast GPT-4
aider --model gpt-4o-mini         # Cost-effective

# Anthropic models
aider --model claude-3-5-sonnet-20241022  # Best overall
aider --model claude-3-haiku-20240307      # Fast and cheap

# Google models
aider --model gemini/gemini-1.5-pro       # Long context

# Local models (requires Ollama)
aider --model ollama/llama3.1:70b        # Local LLaMA
aider --model ollama/mistral:7b          # Local Mistral
```

### Architect Mode

```bash
# Use different models for planning vs editing
aider --architect \
      --model claude-3-5-sonnet-20241022 \
      --editor-model gpt-4o-mini

# Benefits:
# - Claude does complex planning
# - GPT-4o-mini does fast edits
# - Cost-effective and accurate
```

## Configuration Options

### Basic Configuration

```yaml
# .aider.conf.yml
model: claude-3-5-sonnet-20241022
auto-commits: true
dark-mode: true
editor: code
git: true
```

### Advanced Configuration

```yaml
# Full configuration example
model: claude-3-5-sonnet-20241022
editor-model: gpt-4o-mini
auto-commits: true
auto-commit-prefix: "feat:"
dark-mode: true
editor: code
git: true
gitignore: true
map-tokens: 2048
max-chat-history-tokens: 4096
voice: false
suggest-shell-commands: true
```

### Environment Variables

```bash
# Model configuration
export AIDER_MODEL="claude-3-5-sonnet-20241022"
export AIDER_EDITOR_MODEL="gpt-4o-mini"

# Behavior settings
export AIDER_AUTO_COMMITS="true"
export AIDER_DARK_MODE="true"
export AIDER_GITIGNORE="true"

# Token limits
export AIDER_MAP_TOKENS="2048"
export AIDER_MAX_CHAT_HISTORY_TOKENS="4096"
```

## Troubleshooting Common Issues

### API Key Issues

```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Test API connectivity
aider --dry-run "test"

# Check API key format
# OpenAI: sk-...
# Anthropic: sk-ant-...
```

### Git Repository Issues

```bash
# Ensure you're in a git repository
git status

# If not a git repo, initialize
git init
git add .
git commit -m "Initial commit"

# Check git configuration
git config --list | grep user
```

### Python/Installation Issues

```bash
# Check Python version
python --version

# Upgrade pip
pip install --upgrade pip

# Reinstall Aider
pipx uninstall aider-chat
pipx install aider-chat

# Check for conflicts
pip list | grep aider
```

### Model-Specific Issues

```bash
# For Claude: Check API key format
echo $ANTHROPIC_API_KEY | head -c 20

# For local models: Ensure Ollama is running
ollama list
ollama serve

# Test model availability
aider --model ollama/llama3.1:70b --dry-run "test"
```

## Example Project: Simple Web App

Let's create a complete example by building a simple Flask web application:

```bash
# Create project structure
mkdir flask-app
cd flask-app
git init

# Create initial files
cat > app.py << 'EOF'
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
EOF

cat > requirements.txt << 'EOF'
Flask==2.3.3
EOF

# Commit initial version
git add .
git commit -m "Initial Flask app"
```

Now use Aider to enhance it:

```bash
# Start Aider
aider

# Add files
> /add app.py requirements.txt

# Request enhancements
> Add user authentication with Flask-Login, create a user model, and add login/logout routes. Also add SQLAlchemy for database support.
```

Aider will create a comprehensive authentication system with proper models, routes, and database integration.

## Best Practices for Getting Started

### Start Small

```bash
# Begin with simple changes
> Add error handling to this function

# Gradually increase complexity
> Refactor this class to use dependency injection
> Add comprehensive test coverage
```

### Use Git Effectively

```bash
# Always review changes before committing
> /diff

# Use descriptive prompts for better commits
> Implement user registration with email validation and password hashing

# Undo if needed
> /undo
```

### Learn Gradually

```bash
# Start with basic editing
> Fix the typo in line 15

# Progress to architectural changes
> Convert this to use async/await pattern

# Master complex refactoring
> Split this monolithic function into smaller, testable units
```

## Summary

In this chapter, we've covered:

- **Installation**: Multiple ways to install Aider
- **Configuration**: API keys and environment setup
- **First Session**: Making your first AI-powered code changes
- **Workflow**: Understanding Aider's conversation-based approach
- **Models**: Different LLM options and architect mode
- **Troubleshooting**: Common issues and their solutions

## Key Takeaways

1. **Installation**: Use pipx for isolated, clean installation
2. **API Keys**: Configure your preferred LLM provider
3. **File Management**: Use `/add` and `/drop` to control context
4. **Review Changes**: Always use `/diff` before accepting changes
5. **Model Selection**: Choose models based on task complexity and cost
6. **Git Integration**: Aider automatically creates meaningful commits

## Next Steps

Now that you can run Aider and make basic code changes, let's explore **basic editing operations** in the next chapter.

---

**Ready for Chapter 2?** [Basic Editing Operations](02-basic-editing.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*