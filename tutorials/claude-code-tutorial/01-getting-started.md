---
layout: default
title: "Claude Code Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Claude Code Tutorial
---

# Chapter 1: Getting Started with Claude Code

Welcome to **Chapter 1: Getting Started with Claude Code**. In this part of **Claude Code Tutorial: Agentic Coding from Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Claude Code Tutorial: Agentic Coding from Your Terminal**
- tutorial slug: **claude-code-tutorial**
- chapter focus: **Chapter 1: Getting Started with Claude Code**
- system context: **Claude Code Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with Claude Code`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Claude Code Repository](https://github.com/anthropics/claude-code)
- [Claude Code Releases](https://github.com/anthropics/claude-code/releases)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)

### Cross-Tutorial Connection Map

- [Anthropic API Tutorial](../anthropic-code-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Aider Tutorial](../aider-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with Claude Code`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `claude`, `Claude`, `your` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Claude Code` as an operating subsystem inside **Claude Code Tutorial: Agentic Coding from Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `will`, `code`, `project` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Claude Code` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `claude`.
2. **Input normalization**: shape incoming data so `Claude` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `your`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Claude Code Repository](https://github.com/anthropics/claude-code)
  Why it matters: authoritative reference on `Claude Code Repository` (github.com).
- [Claude Code Releases](https://github.com/anthropics/claude-code/releases)
  Why it matters: authoritative reference on `Claude Code Releases` (github.com).
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
  Why it matters: authoritative reference on `Claude Code Docs` (docs.anthropic.com).

Suggested trace strategy:
- search upstream code for `claude` and `Claude` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Basic Commands - Essential Claude Code Operations](02-basic-commands.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
