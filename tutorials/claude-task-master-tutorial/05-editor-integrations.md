---
layout: default
title: "Chapter 5: Editor Integrations"
parent: "Claude Task Master Tutorial"
nav_order: 5
---

# Chapter 5: Editor Integrations

Task Master provides seamless integration with popular code editors, making it a natural part of your development workflow. This chapter covers integration with Cursor, Windsurf, VS Code, and other editors.

## Cursor Integration

### MCP Setup for Cursor

```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "task-master": {
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

### Cursor-Specific Features

```bash
# Enable Task Master in Cursor
# 1. Open Cursor Settings (Cmd/Ctrl + ,)
# 2. Navigate to MCP section
# 3. Enable task-master server
# 4. Restart Cursor

# Test integration
# In Cursor chat: "Show me my current tasks"
# Response should list your active tasks
```

### Cursor Workflow Integration

```bash
# Create task from current file
# In Cursor chat: "Create a task to refactor this React component"

# Link current work to task
# In Cursor chat: "Link this file to task 5"

# Get context-aware suggestions
# In Cursor chat: "What should I work on next in this project?"
```

## Windsurf Integration

### Windsurf MCP Configuration

```json
// ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "task-master": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your-anthropic-key"
      }
    }
  }
}
```

### Windsurf-Specific Commands

```bash
# Enable Task Master integration
# 1. Open Windsurf settings
# 2. Navigate to AI/MCP section
# 3. Add task-master configuration
# 4. Restart Windsurf

# Context-aware task creation
# "Create a task for implementing this API endpoint"
```

## VS Code Integration

### VS Code MCP Setup

```json
// .vscode/mcp.json (project-level)
{
  "servers": {
    "task-master": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your-anthropic-key"
      },
      "type": "stdio"
    }
  }
}

// Or global configuration
// ~/Library/Application Support/Code/User/mcp.json (macOS)
// %APPDATA%/Code/User/mcp.json (Windows)
```

### VS Code Extensions

```json
// .vscode/settings.json
{
  "taskmaster": {
    "enabled": true,
    "autoSync": true,
    "showInStatusBar": true,
    "keyboardShortcuts": {
      "createTask": "ctrl+shift+t",
      "showTasks": "ctrl+shift+l",
      "completeTask": "ctrl+shift+c"
    }
  }
}
```

## General Editor Features

### Universal Commands

```bash
# Available in all integrated editors:

# Task Management
"Show my current tasks"
"Create a new task for [description]"
"Mark task 5 as completed"
"Update task 3 progress to 75%"

# Project Management
"What's the next task I should work on?"
"Show project progress"
"Generate a project report"

# Code Assistance
"Create a task to refactor this function"
"Link current file to task 7"
"Generate tests for this component"
```

### Context-Aware Features

```bash
# File-specific commands
"Create a task for this file"
"Analyze this code and suggest improvements"
"Generate documentation for this module"

# Project-specific commands
"Show project dependencies"
"Identify potential risks"
"Suggest next sprint tasks"
```

## Advanced Integration Features

### Real-Time Synchronization

```json
// Configuration for real-time sync
{
  "taskmaster": {
    "realTimeSync": true,
    "syncInterval": 30000,  // 30 seconds
    "conflictResolution": "manual",
    "offlineSupport": true
  }
}
```

### Git Integration

```bash
# Automatic branch creation
task-master create-branch --from-task 5
# Creates: feature/task-5-implement-auth

# Commit linking
task-master link-commit abc123 --task 5
# Links commit to task for tracking

# PR generation
task-master create-pr --task 5 --template "feature-template"
```

### File System Monitoring

```json
// Monitor file changes
{
  "taskmaster": {
    "fileMonitoring": true,
    "autoTrackChanges": true,
    "changeDetection": {
      "debounceMs": 1000,
      "ignorePatterns": ["node_modules/**", ".git/**"]
    }
  }
}
```

## Custom Editor Extensions

### Building Custom Integrations

```typescript
// custom-editor-extension.ts
import { TaskMasterAPI } from 'task-master-api';

class TaskMasterExtension {
  private api: TaskMasterAPI;

  constructor() {
    this.api = new TaskMasterAPI({
      editor: 'custom-editor',
      version: '1.0.0'
    });
  }

  // Custom commands
  async createTaskFromSelection() {
    const selectedText = this.getSelectedText();
    const task = await this.api.createTask({
      title: `Implement: ${selectedText.substring(0, 50)}...`,
      description: selectedText,
      context: this.getCurrentFileContext()
    });
    return task;
  }

  // Context awareness
  getCurrentFileContext() {
    return {
      filePath: this.getCurrentFile(),
      lineNumber: this.getCurrentLine(),
      projectRoot: this.getProjectRoot(),
      language: this.getFileLanguage()
    };
  }
}
```

### Extension API

```typescript
// Task Master Extension API
interface TaskMasterExtensionAPI {
  // Task operations
  createTask(task: TaskInput): Promise<Task>;
  updateTask(id: string, updates: TaskUpdate): Promise<Task>;
  getTasks(filter?: TaskFilter): Promise<Task[]>;

  // Context operations
  getCurrentContext(): Promise<EditorContext>;
  getProjectStructure(): Promise<ProjectStructure>;

  // Integration hooks
  onFileChange(callback: (change: FileChange) => void): void;
  onTaskUpdate(callback: (task: Task) => void): void;
  onProjectSync(callback: (project: Project) => void): void;
}
```

## IDE-Specific Optimizations

### Cursor Optimizations

```json
// Cursor-specific optimizations
{
  "taskmaster": {
    "cursorOptimizations": {
      "inlineSuggestions": true,
      "contextMenuIntegration": true,
      "statusBarIndicator": true,
      "keyboardShortcuts": {
        "createTask": "cmd+shift+t",
        "quickTask": "cmd+shift+q"
      }
    }
  }
}
```

### VS Code Optimizations

```json
// VS Code-specific features
{
  "taskmaster": {
    "vscodeOptimizations": {
      "treeViewProvider": true,
      "webviewPanels": true,
      "statusBarItems": true,
      "commandPalette": true,
      "workspaceTrust": true
    }
  }
}
```

## Troubleshooting Integration Issues

### Common Problems

```bash
# MCP server not connecting
task-master diagnose-mcp
# Output: Connection test results, suggested fixes

# Editor not recognizing commands
task-master reset-integration --editor cursor
# Reinitializes editor integration

# Sync issues
task-master force-sync
# Forces synchronization of all data
```

### Debug Mode

```bash
# Enable debug logging
task-master debug-mode --enable
# Shows detailed logs for troubleshooting

# View integration logs
task-master logs --filter integration
# Shows editor integration specific logs

# Test editor communication
task-master test-editor-connection
```

## Productivity Enhancements

### Keyboard Shortcuts

```json
// Custom keyboard shortcuts
{
  "taskmaster": {
    "shortcuts": {
      "createTask": "ctrl+alt+t",
      "showTasks": "ctrl+alt+l",
      "completeTask": "ctrl+alt+c",
      "nextTask": "ctrl+alt+n",
      "taskReport": "ctrl+alt+r"
    }
  }
}
```

### Quick Actions

```bash
# Quick task creation from code
# Select code, press shortcut, automatically creates task

# Smart task suggestions
# "What should I work on?" shows context-aware suggestions

# Progress tracking
# Automatic progress updates based on file changes
```

## Enterprise Integration

### Team Features

```json
// Team collaboration settings
{
  "taskmaster": {
    "teamFeatures": {
      "sharedProjects": true,
      "taskAssignments": true,
      "codeReviews": true,
      "timeTracking": true,
      "reporting": true
    }
  }
}
```

### CI/CD Integration

```yaml
# .github/workflows/taskmaster.yml
name: Task Master Integration
on:
  push:
    branches: [main, develop]
jobs:
  sync-tasks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: johnxie/taskmaster-action@v1
        with:
          command: sync
          api-key: ${{ secrets.TASKMASTER_API_KEY }}
```

## Performance Optimization

### Caching Strategies

```json
// Optimize for large projects
{
  "taskmaster": {
    "performance": {
      "enableCaching": true,
      "cacheStrategy": "lru",
      "maxCacheSize": "500MB",
      "preloadCommonTasks": true
    }
  }
}
```

### Lazy Loading

```json
// Load features on demand
{
  "taskmaster": {
    "lazyLoading": {
      "loadOnStartup": ["core", "basic-ui"],
      "loadOnDemand": ["advanced-features", "reporting"],
      "backgroundLoading": true
    }
  }
}
```

## What We've Accomplished

Congratulations! 🎉 You've mastered editor integrations with Task Master:

1. **Cursor Integration** - Seamless MCP setup and workflow integration
2. **Windsurf Integration** - AI-powered development environment integration
3. **VS Code Integration** - Comprehensive extension and MCP support
4. **Universal Commands** - Consistent experience across all editors
5. **Context-Aware Features** - Smart suggestions based on current work
6. **Advanced Features** - Real-time sync, Git integration, file monitoring
7. **Custom Extensions** - Building tailored integrations for specific needs
8. **IDE Optimizations** - Editor-specific performance enhancements
9. **Troubleshooting** - Comprehensive debugging and issue resolution
10. **Productivity Features** - Shortcuts, quick actions, and automation

## Next Steps

Now that you have Task Master fully integrated with your editor, let's explore team collaboration and advanced project management features. In [Chapter 6: Context Control](06-context-control.md), we'll dive into complex project structures, team coordination, and enterprise-level task management.

---

**Practice what you've learned:**
1. Set up Task Master integration in your preferred editor
2. Try creating tasks from code selections
3. Experiment with context-aware commands
4. Set up keyboard shortcuts for common actions

*Which editor do you use most, and what Task Master features would enhance your workflow the most?* 💻
