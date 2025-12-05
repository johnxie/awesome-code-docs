---
layout: default
title: "Aider Tutorial - Chapter 4: Git Integration"
nav_order: 4
has_children: false
parent: Aider Tutorial
---

# Chapter 4: Git Integration

> Master Aider's Git integration features including automatic commits, diffs, undo operations, and version control workflows.

## Overview

Aider has deep Git integration that automatically commits changes, shows diffs, and provides undo capabilities. This chapter covers how to work effectively with Git while using Aider for code editing.

## Automatic Commits

### How Auto-Commits Work

Aider automatically creates Git commits for every accepted change:

```bash
$ aider --auto-commits

# Make a change
> Add a function to calculate fibonacci numbers

# Aider automatically commits:
# feat: Add fibonacci calculation function
```

### Commit Message Generation

Aider generates meaningful commit messages based on your requests:

```bash
# Request: "Fix the bug in user authentication where passwords aren't validated"

# Commit message:
# fix: Validate passwords in user authentication

# Request: "Add rate limiting to API endpoints"

# Commit message:
# feat: Add rate limiting to API endpoints

# Request: "Refactor database connection pooling"

# Commit message:
# refactor: Improve database connection pooling
```

### Configuring Auto-Commits

```bash
# Enable auto-commits (default)
aider --auto-commits

# Disable auto-commits
aider --no-auto-commits

# Custom commit prefix
export AIDER_AUTO_COMMITS="true"
export AIDER_AUTO_COMMIT_PREFIX="feat:"

# Configuration file
cat > .aider.conf.yml << EOF
auto-commits: true
auto-commit-prefix: "feat:"
EOF
```

## Working with Diffs

### Viewing Changes

```bash
# Show what Aider plans to change
> /diff

# Example output:
# app.py
# ```
# --- a/app.py
# +++ b/app.py
# @@ -1,5 +1,8 @@
#  from flask import Flask
# +from flask_limiter import Limiter
# +from flask_limiter.util import get_remote_address
# +
#  app = Flask(__name__)
# +limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per minute"])
# ```

### Understanding Diff Format

```diff
--- a/file.py      # Original file
+++ b/file.py      # Modified file

@@ -1,5 +1,8 @@  # Line numbers: original start, modified start, context length
 from flask import Flask
+from flask_limiter import Limiter     # Added lines start with +
+from flask_limiter.util import get_remote_address
+
 app = Flask(__name__)
+limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per minute"])
```

### Reviewing Before Committing

```bash
# Always review changes
> /diff

# Accept changes
> (press Enter or type 'y')

# Reject changes
> n

# Ask for modifications
> The rate limit should be 50 per minute, not 100

# Aider will adjust and show new diff
```

## Undo Operations

### Undoing the Last Commit

```bash
# Undo the most recent Aider commit
> /undo

# This runs: git reset --hard HEAD~1
# WARNING: This permanently deletes the last commit and its changes
```

### Safe Undo Workflow

```bash
# Before making risky changes, create a backup branch
git checkout -b backup-before-refactor

# Make changes with Aider
> Refactor the entire authentication system

# If you don't like the result
git checkout main  # Go back to main branch
git branch -D backup-before-refactor  # Delete backup if not needed
```

### Selective Undo

```bash
# If you only want to undo part of the last commit
git show HEAD  # See what was changed
git checkout HEAD~1 -- specific-file.py  # Revert only one file
git commit -m "Revert changes to specific-file.py"
```

## Branch Management

### Working with Branches

```bash
# Create a feature branch
git checkout -b feature/user-auth

# Use Aider on the feature branch
aider
> Implement user authentication system

# Switch back to main
git checkout main

# Merge the feature
git merge feature/user-auth
```

### Aider Branch Awareness

Aider is aware of your current branch and includes it in commit messages when relevant:

```bash
# On branch "feature/add-caching"
> Add Redis caching to the API

# Commit message includes branch context:
# feat(feature/add-caching): Add Redis caching to API endpoints
```

## Git Status and History

### Checking Repository State

```bash
# Aider shows git status on startup
Aider v0.50.0
Models: claude-3-5-sonnet-20241022 with diff edit format
Git repo: .git with 12 files  # Repository status
Repo-map: using 1024 tokens

# Check current status
git status

# See recent commits
git log --oneline -5
```

### Working with Uncommitted Changes

```bash
# If you have uncommitted changes, Aider will warn you
git status
# On branch main
# Changes not staged for commit:
#   modified:   app.py

# Aider will ask what to do
# Aider detects uncommitted changes. What would you like to do?
# 1. Commit the changes first
# 2. Stash the changes
# 3. Discard the changes
# 4. Continue anyway
```

## Advanced Git Workflows

### Interactive Rebase with Aider

```bash
# Create several commits with Aider
> Add user model
> Add authentication routes
> Add password hashing

# Then interactively rebase to clean up commits
git rebase -i HEAD~3

# Squash related commits together
pick abc123 feat: Add user model
squash def456 feat: Add authentication routes
squash ghi789 feat: Add password hashing
```

### Git Hooks Integration

```bash
# Pre-commit hook to run tests before Aider commits
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running tests before commit..."
if ! python -m pytest tests/ -v; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

### Working with Git Flow

```bash
# Feature branch workflow
git checkout -b feature/new-feature
aider
> Implement the new feature

# Create pull request
git push -u origin feature/new-feature
# Create PR on GitHub/GitLab

# After review, merge
git checkout main
git merge feature/new-feature
```

## Conflict Resolution

### Handling Merge Conflicts

```bash
# If you get merge conflicts after pulling
git pull origin main
# Auto-merging app.py
# CONFLICT (content): Merge conflict in app.py

# Use Aider to resolve conflicts
aider
> /add app.py
> Resolve the merge conflict by keeping both authentication methods
```

### Preventing Conflicts

```bash
# Work on feature branches
git checkout -b feature/auth-improvements

# Pull latest changes frequently
git pull origin main

# Communicate with team about who is working on what files
```

## Gitignore Management

### Aider and Gitignore

Aider respects your `.gitignore` file and won't suggest adding ignored files to the repository.

```bash
# Aider won't suggest committing these files
.env
__pycache__/
*.pyc
.DS_Store
```

### Managing Sensitive Files

```bash
# If Aider accidentally suggests sensitive files
> Never add .env files or API keys to the repository

# Aider will respect .gitignore
echo ".env" >> .gitignore
echo "secrets/" >> .gitignore
```

## Commit Message Best Practices

### Conventional Commits

```bash
# Aider follows conventional commit format
type(scope): description

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation
# style: Code style changes
# refactor: Code refactoring
# test: Adding tests
# chore: Maintenance tasks
```

### Customizing Commit Messages

```bash
# Add issue references
> Fix the login bug #123

# Commit: fix: Resolve login authentication issue (#123)

# Add scope
export AIDER_AUTO_COMMIT_PREFIX="feat(auth):"

# Commit: feat(auth): Add OAuth integration
```

## Working with Large Codebases

### Selective File Management

```bash
# Only work on specific parts of large codebase
> /add auth/ models/user.py services/auth_service.py

# Don't modify other parts
> Refactor the authentication system but don't touch the payment code
```

### Repository Mapping Optimization

```bash
# For large repos, adjust repo-map tokens
export AIDER_MAP_TOKENS="4096"  # Increase context

# Or focus on specific directories
aider --map-tokens 2048
```

## Backup and Recovery

### Creating Safety Checkpoints

```bash
# Before major refactoring
git tag backup-before-refactor-$(date +%Y%m%d_%H%M%S)

# Or create backup branch
git checkout -b backup-$(date +%Y%m%d_%H%M%S)
git checkout main
```

### Recovery Procedures

```bash
# If something goes wrong
git reflog  # See recent actions
git reset --hard HEAD@{1}  # Go back one step

# Or revert specific commits
git revert abc123 def456  # Revert specific commits
```

## Integration with Git Hosting

### GitHub Integration

```bash
# Create PR from Aider commits
git push -u origin feature/new-feature

# GitHub will show commits created by Aider
# feat: Add user authentication
# feat: Add password validation
# feat: Add session management
```

### GitLab Integration

```bash
# Similar workflow for GitLab
git push -u origin feature/new-feature

# Create merge request with Aider-generated commits
```

## Summary

In this chapter, we've covered:

- **Automatic Commits**: How Aider creates Git commits for every change
- **Diff Review**: Understanding and reviewing changes before committing
- **Undo Operations**: Safely reverting Aider's changes
- **Branch Management**: Working with Git branches and workflows
- **Conflict Resolution**: Handling merge conflicts and preventing them
- **Gitignore**: Managing which files Aider should ignore
- **Commit Messages**: Best practices for meaningful commit messages
- **Large Codebases**: Strategies for working with big repositories
- **Backup and Recovery**: Safety procedures for risky operations

## Key Takeaways

1. **Review Changes**: Always use `/diff` before accepting changes
2. **Auto-Commits**: Aider automatically creates meaningful commits
3. **Safe Undo**: Use `/undo` carefully and create backups for risky changes
4. **Branch Workflow**: Use feature branches for organized development
5. **Conflict Prevention**: Pull frequently and communicate with team
6. **Conventional Commits**: Follow standard commit message formats

## Next Steps

Now that you understand Git integration, let's explore **advanced prompting techniques** to get better results from Aider.

---

**Ready for Chapter 5?** [Advanced Prompting](05-prompting.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*