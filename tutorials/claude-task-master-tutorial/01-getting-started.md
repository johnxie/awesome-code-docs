---
layout: default
title: "Chapter 1: Getting Started with Claude Task Master"
parent: "Claude Task Master Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Claude Task Master

Welcome to Claude Task Master! If you've ever struggled with breaking down complex projects into manageable tasks, or wished you had an AI assistant to help manage your development workflow, you're in the right place. Task Master transforms how developers approach project planning and execution with intelligent AI-powered task management.

## What Makes Task Master Special?

Task Master revolutionizes project management by:
- **AI-Powered Analysis** - Converts requirements into detailed task breakdowns
- **Multi-Editor Support** - Works seamlessly with Cursor, Windsurf, VS Code, and more
- **Intelligent Planning** - Creates realistic timelines and dependency mapping
- **Context Awareness** - Maintains project context across all tasks
- **Progress Tracking** - Monitors completion and suggests next steps
- **Team Collaboration** - Supports shared project management

## Installation Options

### Option 1: MCP Integration (Recommended)

MCP (Model Control Protocol) provides the most seamless integration with your editor:

#### For Cursor
```bash
# Add to your MCP configuration
# ~/.cursor/mcp.json or .cursor/mcp.json in project
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your-anthropic-key",
        "OPENAI_API_KEY": "your-openai-key",
        "PERPLEXITY_API_KEY": "your-perplexity-key"
      }
    }
  }
}
```

#### For Windsurf
```bash
# Add to your Windsurf MCP configuration
# ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your-anthropic-key",
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

#### For VS Code
```bash
# Add to your VS Code MCP configuration
# .vscode/mcp.json in project
{
  "servers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your-anthropic-key"
      },
      "type": "stdio"
    }
  }
}
```

### Option 2: Local Installation

```bash
# Install globally
npm install -g task-master-ai

# Or install locally in your project
npm install task-master-ai

# Verify installation
task-master --version
```

## Your First Project Setup

Let's create your first AI-managed project:

### Step 1: Initialize Task Master

```bash
# Initialize in your project directory
cd your-project-directory
task-master init

# Or use with MCP (recommended)
# In your editor's AI chat, type:
# "Initialize taskmaster-ai in my project"
```

### Step 2: Create a Project Requirements Document (PRD)

Task Master works best with a detailed PRD. Create `.taskmaster/docs/prd.txt`:

```txt
# E-commerce Platform PRD

## Overview
Build a modern e-commerce platform with the following features:
- User authentication and profiles
- Product catalog with search and filtering
- Shopping cart and checkout system
- Order management and tracking
- Admin dashboard for inventory management

## Technical Requirements
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL
- Authentication: JWT tokens
- Payment: Stripe integration

## Target Users
- End customers looking for products
- Business owners managing their store
- Administrators overseeing the platform

## Success Metrics
- Support 1000+ concurrent users
- Process payments securely
- Maintain 99.9% uptime
- Complete orders within 24 hours

## Timeline
- MVP: 3 months
- Full launch: 6 months
```

### Step 3: Parse Your Requirements

```bash
# Parse the PRD and generate tasks
task-master parse-prd .taskmaster/docs/prd.txt

# Or use MCP command in your editor:
# "Can you parse my PRD at .taskmaster/docs/prd.txt?"
```

### Step 4: Review Generated Tasks

```bash
# List all generated tasks
task-master list

# View specific tasks
task-master show 1,2,3

# Or use MCP:
# "Can you show me tasks 1, 2, and 3?"
```

## Understanding Task Master Architecture

### Core Components

```
Task Master System
├── AI Engine (Claude/OpenAI/GPT)
├── Task Parser (PRD → Tasks)
├── Task Manager (CRUD operations)
├── Dependency Resolver (Task relationships)
├── Progress Tracker (Completion monitoring)
└── Editor Integration (MCP/WebSocket)
```

### Task Structure

Each task contains:
- **ID**: Unique identifier
- **Title**: Clear, actionable description
- **Description**: Detailed requirements and context
- **Dependencies**: Tasks that must be completed first
- **Priority**: High, Medium, Low
- **Estimated Time**: Time estimate in hours
- **Status**: Pending, In Progress, Completed, Blocked
- **Assigned To**: Team member or AI agent

### Task Dependencies

```json
{
  "task_1": {
    "title": "Set up project structure",
    "dependencies": [],
    "estimated_hours": 2,
    "status": "completed"
  },
  "task_2": {
    "title": "Implement user authentication",
    "dependencies": ["task_1"],
    "estimated_hours": 8,
    "status": "in_progress"
  },
  "task_3": {
    "title": "Create user profile pages",
    "dependencies": ["task_2"],
    "estimated_hours": 6,
    "status": "pending"
  }
}
```

## Working with Tasks

### Basic Task Operations

```bash
# Start working on a task
task-master start 2

# Mark task as completed
task-master complete 2

# Update task description
task-master update 2 --description "New description"

# Add time spent
task-master log 2 --hours 3

# Or use MCP commands:
# "Can you start working on task 2?"
# "Mark task 2 as completed"
```

### Task Filtering and Search

```bash
# Show only pending tasks
task-master list --status pending

# Show high priority tasks
task-master list --priority high

# Search tasks by keyword
task-master search "authentication"

# Show tasks assigned to you
task-master list --assigned-to me
```

### Dependency Management

```bash
# Add dependency between tasks
task-master dependency add 5 --depends-on 2,3

# Remove dependency
task-master dependency remove 5 --depends-on 2

# View task dependencies
task-master show 5 --dependencies

# Show dependency graph
task-master graph
```

## AI-Powered Features

### Intelligent Task Breakdown

Task Master uses AI to:
- **Analyze Complexity**: Determine task difficulty and time estimates
- **Identify Dependencies**: Automatically detect task relationships
- **Suggest Prioritization**: Recommend task execution order
- **Generate Descriptions**: Create detailed task descriptions
- **Estimate Time**: Provide realistic time estimates

### Smart Suggestions

```bash
# Get next recommended task
task-master next

# Get suggestions for current task
task-master suggest 2

# Analyze project progress
task-master analyze

# Or use MCP:
# "What's the next task I should work on?"
# "Can you suggest improvements for task 2?"
```

### Research Integration

```bash
# Research specific technologies
task-master research "React best practices for e-commerce"

# Research implementation approaches
task-master research "JWT authentication patterns"

# Get fresh information for current task
task-master research --task 3 "payment integration security"

# Or use MCP:
# "Research the latest best practices for implementing JWT authentication"
```

## Multi-Model Support

Task Master supports multiple AI models for different purposes:

### Main Model (Claude/OpenAI)
- Task planning and breakdown
- Code generation and review
- Architecture decisions

### Research Model (Perplexity/OpenAI)
- Information gathering
- Technology research
- Best practices lookup

### Fallback Model
- Backup when primary models are unavailable
- Cost-effective task management

```bash
# Configure different models
task-master config --main-model claude-3-5-sonnet-20241022
task-master config --research-model gpt-4o
task-master config --fallback-model gpt-3.5-turbo
```

## Real-World Project Example

### E-commerce Platform Development

```bash
# 1. Initialize project
task-master init

# 2. Create detailed PRD
echo "Build a full-stack e-commerce platform with React, Node.js, PostgreSQL" > .taskmaster/docs/prd.txt

# 3. Generate tasks
task-master parse-prd .taskmaster/docs/prd.txt

# 4. Review and adjust tasks
task-master list
task-master update 1 --priority high

# 5. Start development
task-master start 1
task-master complete 1

# 6. Get next task
task-master next

# 7. Research as needed
task-master research "React e-commerce best practices"
```

### Task Output Example

```
📋 Generated Tasks for E-commerce Platform

1. ✅ Set up project structure and dependencies (2h)
2. 🔄 Implement user authentication system (8h)
3. ⏳ Create product catalog with search (6h)
4. ⏳ Build shopping cart functionality (4h)
5. ⏳ Integrate payment processing (6h)
6. ⏳ Develop admin dashboard (8h)
7. ⏳ Set up deployment pipeline (4h)

Dependencies:
- Task 3 depends on Task 2
- Task 4 depends on Task 3
- Task 5 depends on Task 4
- Task 6 depends on Task 2,3
- Task 7 depends on all previous tasks
```

## Integration with Development Workflow

### Editor Integration

```bash
# Enable MCP in your editor
# Cursor: Settings → MCP → Enable task-master-ai
# Windsurf: Similar MCP configuration
# VS Code: Add MCP server configuration

# Now you can use natural language commands:
# "What's the next task I should work on?"
# "Can you help me implement task 3?"
# "Research React hooks best practices"
```

### Git Integration

```bash
# Create branches for tasks
task-master branch 3  # Creates branch for task 3

# Commit with task reference
git commit -m "feat: implement user auth (#task-2)"

# Link commits to tasks
task-master link-commit abc123 --task 2
```

### Team Collaboration

```bash
# Assign tasks to team members
task-master assign 3 --to alice@example.com
task-master assign 4 --to bob@example.com

# Share project status
task-master share --format markdown > project-status.md

# Export for external tools
task-master export --format json > tasks.json
```

## Configuration and Customization

### Basic Configuration

```bash
# Set your preferences
task-master config --timezone America/New_York
task-master config --working-hours "9-17"
task-master config --default-priority medium

# API key management
task-master config --anthropic-key your-key-here
task-master config --openai-key your-key-here
```

### Advanced Configuration

```json
// .taskmaster/config.json
{
  "models": {
    "main": "claude-3-5-sonnet-20241022",
    "research": "gpt-4o",
    "fallback": "gpt-3.5-turbo"
  },
  "preferences": {
    "autoResearch": true,
    "suggestionsEnabled": true,
    "dependencyChecking": true,
    "progressTracking": true
  },
  "integrations": {
    "github": {
      "enabled": true,
      "autoBranch": true,
      "autoCommit": false
    },
    "slack": {
      "enabled": false,
      "webhook": ""
    }
  }
}
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Claude Task Master** and integrated it with your editor
2. **Created your first AI-managed project** with intelligent task breakdown
3. **Learned the core architecture** and task management system
4. **Explored AI-powered features** for research and planning
5. **Set up multi-model support** for different types of tasks
6. **Integrated with your development workflow** using MCP
7. **Configured Task Master** for your specific needs and preferences

## Next Steps

Now that you have Task Master set up, let's dive deeper into how it analyzes requirements and generates tasks. In [Chapter 2: PRD Analysis & Task Generation](02-prd-analysis.md), we'll explore how to write effective PRDs and leverage Task Master's AI for optimal task breakdown.

---

**Practice what you've learned:**
1. Create a PRD for a project you're working on
2. Use Task Master to generate and organize tasks
3. Experiment with the research feature for your current task
4. Try the MCP integration with natural language commands

*What's the most complex project you've managed, and how could Task Master help?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `task`, `master`, `your` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Claude Task Master` as an operating subsystem inside **Claude Task Master Tutorial: AI-Powered Task Management for Developers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `tasks`, `Task`, `project` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Claude Task Master` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `task`.
2. **Input normalization**: shape incoming data so `master` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `your`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/eyaltoledano/claude-task-master)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `task` and `master` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: PRD Analysis & Task Generation](02-prd-analysis.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
