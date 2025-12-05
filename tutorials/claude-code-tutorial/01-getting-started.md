---
layout: default
title: "Claude Code Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Claude Code Tutorial
---

# Chapter 1: Getting Started with Claude Code

> Install Claude Code, authenticate with Anthropic, and start your first AI-powered coding session.

## Overview

This chapter guides you through installing Claude Code, setting up authentication, and running your first interactive coding session. Claude Code is Anthropic's agentic coding tool that brings Claude's intelligence directly to your terminal.

## Installation

### System Requirements

```bash
# Operating Systems
- macOS 12.0 or later
- Linux (Ubuntu 18.04+, CentOS 7+, etc.)
- Windows 10/11 (via WSL)

# Software Requirements
- Node.js 18.0 or later
- npm 8.0 or later
- Git (for repository operations)

# Hardware Requirements
- 4GB RAM minimum, 8GB recommended
- 2GB disk space for installation
```

### Installing Node.js and npm

```bash
# Check current Node.js version
node --version
npm --version

# If not installed or outdated, install Node.js 18+
# On macOS with Homebrew
brew install node@18

# On Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# On CentOS/RHEL/Fedora
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs  # or dnf/zypper

# On Windows (PowerShell as Administrator)
# Download from https://nodejs.org/ and install

# Verify installation
node --version  # Should show v18.x.x
npm --version   # Should show 8.x.x or higher
```

### Installing Claude Code

```bash
# Install globally via npm
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version

# Check if it's working
claude --help
```

### Alternative Installation Methods

```bash
# Install specific version
npm install -g @anthropic-ai/claude-code@0.1.0

# Install from GitHub releases (manual)
# Download the appropriate binary from:
# https://github.com/anthropics/claude-code/releases

# For Linux/macOS
chmod +x claude-code
sudo mv claude-code /usr/local/bin/claude

# For Windows, add to PATH
```

### Troubleshooting Installation

```bash
# Permission issues
sudo npm install -g @anthropic-ai/claude-code

# npm cache issues
npm cache clean --force
npm install -g @anthropic-ai/claude-code

# Node version conflicts
nvm use 18  # If using nvm
npm install -g @anthropic-ai/claude-code

# Verify PATH
which claude
echo $PATH | grep -o '/usr/local/bin'

# Check npm permissions
npm config get prefix
```

## Authentication

### Anthropic API Key Setup

```bash
# Method 1: Claude Pro subscription (recommended)
# If you have Claude Pro, Claude Code will use it automatically

# Method 2: Anthropic API key
# Get API key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"

# Make it permanent
echo 'export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"' >> ~/.zshrc

# For Windows
setx ANTHROPIC_API_KEY "sk-ant-your-api-key-here"
```

### Authentication Command

```bash
# Authenticate Claude Code
claude auth login

# This will:
# 1. Check for existing authentication
# 2. Guide you through login process
# 3. Store credentials securely

# Verify authentication
claude auth status
```

### Authentication Methods

```bash
# Option 1: Claude Pro (automatic)
# If you have Claude Pro, no additional setup needed
claude auth login  # Will detect Claude Pro

# Option 2: API Key (manual)
claude auth login --api-key

# Option 3: Environment variable
export ANTHROPIC_API_KEY="your-key"
claude auth login

# Option 4: Configuration file
echo 'apiKey: "sk-ant-your-key"' > ~/.claude/config.yaml
claude auth login --config ~/.claude/config.yaml
```

### Testing Authentication

```bash
# Test with a simple command
claude "hello world"

# Should respond with a greeting and confirm authentication

# Check authentication status
claude auth status

# Output should show:
# ✓ Authenticated with Anthropic
# Account: your-email@domain.com
# Plan: Claude Pro (or API Key)
```

## Your First Session

### Starting Claude Code

```bash
# Navigate to a project directory
cd your-coding-project

# Start interactive session
claude

# You should see:
# ╭─────────────────────────────────────────────╮
# │ Claude Code                                  │
# │ Type your request or /help for commands     │
# ╰─────────────────────────────────────────────╯
# >
```

### Basic Interaction

```bash
# Your first command
> What does this project do?

# Claude will analyze your codebase and respond

# Try a simple task
> Create a new file called hello.py with a simple hello world function

# Claude will create the file and show you the changes
```

### Understanding the Interface

```bash
# The interface shows:
# - Current directory and project context
# - Available commands (type /help)
# - Conversation history
# - File changes and command outputs

# Example session:
$ claude
╭─────────────────────────────────────────────╮
│ Claude Code                                  │
│ Type your request or /help for commands     │
╰─────────────────────────────────────────────╯

> What files are in this project?
Analyzing project structure...
Found 12 files in your project:
- package.json
- src/index.ts
- src/utils.ts
- tests/
- README.md

This appears to be a TypeScript npm package for data processing utilities.

>
```

## Project Analysis

### Codebase Understanding

```bash
# Claude analyzes your project automatically
> Tell me about this codebase

# Claude will read:
# - package.json (dependencies, scripts)
# - README.md (project description)
# - Main source files
# - Configuration files
# - Test files

# And provide a comprehensive overview
```

### File Exploration

```bash
# Ask about specific files
> What does src/index.ts contain?

# Claude will read and explain the file

# Explore directory structure
> Show me the test directory structure

# Claude will list and describe test files
```

### Technology Stack Detection

```bash
# Claude automatically detects:
# - Programming languages (TypeScript, Python, etc.)
# - Frameworks (React, Express, Django, etc.)
# - Build tools (npm, yarn, webpack, etc.)
# - Testing frameworks (Jest, pytest, etc.)
# - Database systems
# - Deployment configurations

> What technologies does this project use?
```

## Basic Commands

### Help System

```bash
# Get help
> /help

# Shows available commands:
/help - Show this help message
/clear - Clear conversation history
/compact - Reduce context size
/cost - Show token usage and cost
/quit - Exit Claude Code

# Command-specific help
> /help clear
```

### Session Management

```bash
# Clear conversation history
> /clear

# This removes all previous context
# Useful for starting fresh or reducing token usage

# Compact context (keep recent messages)
> /compact

# Reduces context size while preserving recent conversation
```

### Cost Tracking

```bash
# Check usage and costs
> /cost

# Shows:
# - Total tokens used in session
# - Estimated cost
# - Token breakdown (input/output)
```

### Exiting Sessions

```bash
# Exit Claude Code
> /quit

# Or use Ctrl+C (may require confirmation)

# Safe exit (preserves conversation)
> /quit
# Conversation saved. Run 'claude' to continue.
```

## One-Off Commands

### Running Single Commands

```bash
# Run a single command without interactive session
claude "explain the main function in src/index.ts"

# Useful for quick queries without full session

# Complex one-off tasks
claude "find all TODO comments in the codebase and summarize them"

# File operations
claude "create a new test file for the user authentication feature"
```

### Scripting with Claude Code

```bash
# Use in scripts
#!/bin/bash
# analyze_code.sh

echo "Analyzing codebase..."
claude "provide a summary of all the functions in src/" > analysis.txt

echo "Checking for security issues..."
claude "scan the codebase for potential security vulnerabilities" > security.txt

echo "Analysis complete!"
```

## Safety Features

### Approval System

```bash
# Claude asks for approval before making changes
> Add error handling to the API routes

# Claude will show proposed changes and ask:
# Shall I proceed with these changes? [Y/n]

# You can:
# - Press 'y' to approve
# - Press 'n' to reject
# - Provide feedback for modifications
```

### Command Safety

```bash
# Dangerous commands require confirmation
> Run the database migrations

# Claude will show the command and ask for confirmation:
# I'm about to run: npm run migrate
# This command will modify your database. Proceed? [Y/n]
```

### Undo Capability

```bash
# Claude can undo recent changes
> Undo the last change

# This will revert the most recent file modification
# Note: This doesn't affect Git commits
```

## Error Handling

### Common Errors

```bash
# Authentication errors
claude auth login
# Error: Invalid API key
# Solution: Check your ANTHROPIC_API_KEY

# Network errors
# Error: Connection failed
# Solution: Check internet connection and Anthropic API status

# File permission errors
# Error: Cannot write to file
# Solution: Check file permissions and git status
```

### Recovery Strategies

```bash
# If Claude gets stuck
> /clear
# Clears conversation and starts fresh

# If context is too large
> /compact
# Reduces context size

# If you want to start over
> /quit
# Exit and restart session
```

## Best Practices for Getting Started

### Start Small

```bash
# Begin with simple tasks
> What does this project do?
> Show me the main entry point
> Explain the database schema

# Gradually increase complexity
> Add input validation to the API
> Create unit tests for the utility functions
> Refactor the authentication logic
```

### Use Git Wisely

```bash
# Commit before major changes
git add .
git commit -m "Before Claude Code changes"

# Let Claude make changes
# Claude will create its own commits

# Review Claude's commits
git log --oneline -5
```

### Keep Sessions Focused

```bash
# Work on one feature at a time
> Implement user registration
# Complete this feature before starting another

# Clear context between unrelated tasks
> /clear
> Now let's work on the payment system
```

### Learn from Claude

```bash
# Ask for explanations
> Why did you structure the code this way?
> What are the trade-offs of this approach?

# Request best practices
> How should I organize the error handling?
> What testing patterns should I use?

# Get code reviews
> Review this code for potential improvements
```

## Summary

In this chapter, we've covered:

- **Installation**: Setting up Node.js, npm, and Claude Code
- **Authentication**: Connecting with Anthropic API or Claude Pro
- **First Session**: Starting interactive coding sessions
- **Project Analysis**: How Claude understands your codebase
- **Basic Commands**: Help, clear, cost, and quit operations
- **One-Off Commands**: Running single commands without sessions
- **Safety Features**: Approval system, command confirmation, and undo
- **Error Handling**: Common issues and recovery strategies

## Key Takeaways

1. **Easy Setup**: Install with npm and authenticate with Anthropic
2. **Project Aware**: Claude automatically analyzes your codebase
3. **Interactive**: Natural conversation-based development
4. **Safe Changes**: Approval system prevents unwanted modifications
5. **Cost Tracking**: Monitor token usage and expenses
6. **Flexible Usage**: Both interactive sessions and one-off commands

## Next Steps

Now that you can run Claude Code, let's explore the **basic commands** and operations available in the next chapter.

---

**Ready for Chapter 2?** [Basic Commands](02-basic-commands.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*