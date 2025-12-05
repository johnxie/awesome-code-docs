---
layout: default
title: "Aider Tutorial"
nav_order: 80
has_children: true
---

# Aider Tutorial: AI Pair Programming in Your Terminal

> Collaborate with AI to edit code in your local git repository.

<div align="center">

**👨‍💻 AI Pair Programming That Actually Works**

[![GitHub](https://img.shields.io/github/stars/Aider-AI/aider?style=social)](https://github.com/Aider-AI/aider)

</div>

---

## 🎯 What is Aider?

**Aider**<sup>[View Repo](https://github.com/Aider-AI/aider)</sup> is an AI pair programming tool that runs in your terminal. It lets you chat with GPT-4, Claude, or other LLMs to edit code in your local git repository. Unlike other AI coding tools, Aider makes real changes to your actual files and creates git commits.

### Why Aider?

| Feature | Description |
|:--------|:------------|
| **Real File Edits** | Changes your actual files, not just suggestions |
| **Git Integration** | Automatic commits with descriptive messages |
| **Multi-File Editing** | Edit multiple files in a single conversation |
| **Voice Support** | Dictate coding instructions |
| **Model Flexibility** | Works with GPT-4, Claude, local models |
| **Context Awareness** | Understands your entire codebase |

```mermaid
flowchart LR
    A[Your Prompt] --> B[Aider]
    B --> C[LLM]
    C --> D[Edit Plan]
    D --> E[Apply Changes]
    E --> F[Your Files]
    F --> G[Git Commit]
    
    classDef user fill:#e1f5fe,stroke:#01579b
    classDef aider fill:#f3e5f5,stroke:#4a148c
    classDef files fill:#e8f5e8,stroke:#1b5e20
    
    class A user
    class B,C,D,E aider
    class F,G files
```

## Tutorial Chapters

1. **[Chapter 1: Getting Started](01-getting-started.md)** - Installation, setup, and your first Aider session
2. **[Chapter 2: Basic Editing](02-basic-editing.md)** - Adding, editing, and deleting code
3. **[Chapter 3: Multi-File Projects](03-multi-file.md)** - Working across multiple files
4. **[Chapter 4: Git Integration](04-git.md)** - Commits, diffs, and version control
5. **[Chapter 5: Advanced Prompting](05-prompting.md)** - Getting the best results from AI
6. **[Chapter 6: Model Configuration](06-models.md)** - Using different LLM providers
7. **[Chapter 7: Voice & Workflows](07-workflows.md)** - Voice input and automation
8. **[Chapter 8: Best Practices](08-best-practices.md)** - Tips for effective AI pair programming

## What You'll Learn

- **Edit Code with AI** in your actual files
- **Use Git Effectively** with automatic commits
- **Work Across Files** in complex projects
- **Configure Models** for different tasks
- **Prompt Effectively** for best results
- **Integrate Voice** for hands-free coding
- **Build Workflows** for repetitive tasks

## Prerequisites

- Python 3.8+
- Git installed and configured
- API key for your LLM provider
- A code project to work on

## Quick Start

```bash
# Install Aider
pip install aider-chat

# Or with pipx (recommended)
pipx install aider-chat

# Set your API key
export OPENAI_API_KEY="sk-..."

# Or for Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Your First Session

```bash
# Navigate to your project
cd my-project

# Start Aider with GPT-4o
aider

# Or specify a model
aider --model claude-3-5-sonnet-20241022

# Add files to the chat
> /add src/main.py src/utils.py

# Make a request
> Add a function to calculate fibonacci numbers in utils.py
```

## Key Commands

| Command | Description |
|:--------|:------------|
| `/add <file>` | Add file(s) to the chat context |
| `/drop <file>` | Remove file(s) from context |
| `/ls` | List files in the chat |
| `/diff` | Show pending changes |
| `/undo` | Undo the last git commit |
| `/clear` | Clear the chat history |
| `/help` | Show all commands |

## Example Session

```
$ cd my-flask-app
$ aider

Aider v0.50.0
Models: claude-3-5-sonnet-20241022 with diff edit format
Git repo: .git with 12 files
Repo-map: using 1024 tokens

> /add app.py routes/api.py

Added app.py to the chat.
Added routes/api.py to the chat.

> Add rate limiting to the API routes. Use Flask-Limiter with 100 requests per minute per IP.

I'll add rate limiting using Flask-Limiter. Here are the changes:

app.py
<<<<<<< SEARCH
from flask import Flask

app = Flask(__name__)
=======
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)
>>>>>>> REPLACE

routes/api.py
<<<<<<< SEARCH
@api.route('/users', methods=['GET'])
def get_users():
=======
from app import limiter

@api.route('/users', methods=['GET'])
@limiter.limit("100 per minute")
def get_users():
>>>>>>> REPLACE

Commit: feat: Add rate limiting with Flask-Limiter (100 req/min per IP)
```

## Model Configuration

```bash
# OpenAI GPT-4o (default)
aider --model gpt-4o

# Anthropic Claude
aider --model claude-3-5-sonnet-20241022

# Local model with Ollama
aider --model ollama/llama3.1:70b

# Azure OpenAI
aider --model azure/my-deployment

# Using config file
cat > .aider.conf.yml << EOF
model: claude-3-5-sonnet-20241022
auto-commits: true
dark-mode: true
EOF
```

## Architect Mode

For complex changes, use architect mode with a smart model for planning and a fast model for editing:

```bash
# Claude for architecture, GPT-4o-mini for edits
aider --architect --model claude-3-5-sonnet-20241022 --editor-model gpt-4o-mini
```

## Voice Mode

```bash
# Enable voice input
aider --voice

# Speak your changes, Aider transcribes and executes
# "Add a new endpoint for user registration that validates email format"
```

## Tips for Effective Use

### Be Specific
```
# ❌ Vague
> Fix the bug

# ✅ Specific
> Fix the bug in user_auth.py where the password hash comparison
> fails for passwords containing special characters
```

### Provide Context
```
# ❌ No context
> Add caching

# ✅ With context
> Add Redis caching to the get_user_profile function.
> Cache for 5 minutes. The Redis client is already configured in config.py
```

### Review Changes
```
> /diff  # See what Aider wants to change before committing
> /undo  # Revert if something went wrong
```

## Supported Models

| Provider | Models | Best For |
|:---------|:-------|:---------|
| **Anthropic** | Claude 3.5 Sonnet | Best overall performance |
| **OpenAI** | GPT-4o, GPT-4-turbo | Good all-rounder |
| **Google** | Gemini 1.5 Pro | Long context |
| **Local** | LLaMA, Mistral via Ollama | Privacy, offline use |

## Learning Path

### 🟢 Beginner Track
1. Chapters 1-3: Setup and basic editing
2. Make simple code changes with AI

### 🟡 Intermediate Track
1. Chapters 4-6: Git, prompting, and models
2. Integrate Aider into your workflow

### 🔴 Advanced Track
1. Chapters 7-8: Voice, automation, and best practices
2. Master AI pair programming

---

**Ready to pair program with AI? Let's begin with [Chapter 1: Getting Started](01-getting-started.md)!**

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
