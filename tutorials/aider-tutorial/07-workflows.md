---
layout: default
title: "Aider Tutorial - Chapter 7: Voice & Workflows"
nav_order: 7
has_children: false
parent: Aider Tutorial
---

# Chapter 7: Voice & Workflows

> Use voice input for hands-free coding and create automated workflows for repetitive tasks.

## Overview

Aider supports voice input and workflow automation to streamline development. This chapter covers voice coding, custom workflows, and automation techniques.

## Voice Input Setup

### System Requirements

```bash
# macOS (built-in)
# No additional setup needed

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# Windows
pip install pyaudio
# May need additional audio drivers
```

### Enabling Voice Mode

```bash
# Start Aider with voice support
aider --voice

# Or enable in configuration
cat > .aider.conf.yml << EOF
voice: true
EOF

# Voice indicator in prompt
Aider v0.50.0 [voice]
>
```

### Voice Commands

```bash
# Basic voice interaction
> "Add a function to calculate the fibonacci sequence"

# Aider transcribes and processes
# Added fibonacci calculation function

# Voice with code dictation
> "Create a class called User with attributes name, email, and age"

# Voice for complex instructions
> "Refactor this function to use async/await pattern and add proper error handling"
```

## Voice Best Practices

### Clear Speech Techniques

```bash
# Speak clearly and at normal pace
> "Add input validation to the login form"

# Use pauses for complex terms
> "Create a function that validates email addresses using regular expressions"

# Spell out unusual terms
> "Add a route for user registration with B-Crypt password hashing"
```

### Voice Command Patterns

```bash
# Action + Object + Details
> "Create a new file called utils.py with helper functions"

# Modify + Target + Changes
> "Modify the user model to add a created_at timestamp field"

# Add + Feature + Context
> "Add error handling to the database connection with retry logic"
```

### Voice Feedback

```bash
# Aider confirms voice commands
> "Add type hints to all functions"
# Transcribed: "Add type hints to all functions"
# Processing request...

# Ask for confirmation on complex changes
> "Refactor the entire authentication system"
# This will make significant changes. Are you sure? (y/n)
```

## Workflow Automation

### Custom Scripts and Aliases

```bash
# Create reusable workflow scripts
cat > workflows/setup-new-feature.sh << 'EOF'
#!/bin/bash
# Setup script for new features

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

# Create branch
git checkout -b "$BRANCH_NAME"

# Start Aider with feature context
aider --model claude-3-5-sonnet-20241022 \
      --auto-commits \
      --message "feat: Start $FEATURE_NAME implementation"

echo "Ready to implement $FEATURE_NAME on branch $BRANCH_NAME"
EOF

chmod +x workflows/setup-new-feature.sh

# Usage
./workflows/setup-new-feature.sh user-authentication
```

### Pre-configured Sessions

```bash
# Development workflow
cat > dev-workflow.sh << 'EOF'
#!/bin/bash
# Daily development workflow

echo "Starting development session..."

# Ensure on main branch and up to date
git checkout main
git pull origin main

# Start Aider with development settings
aider --model gpt-4o-mini \
      --auto-commits \
      --dark-mode \
      --voice \
      --message "chore: Daily development work"

echo "Development session ready. Speak or type your requests."
EOF

chmod +x dev-workflow.sh
```

### Automated Testing Workflows

```bash
# Test-driven development workflow
cat > tdd-workflow.sh << 'EOF'
#!/bin/bash
# Test-driven development workflow

echo "Starting TDD workflow..."

# Run existing tests
if ! python -m pytest tests/ -v; then
    echo "Existing tests failing. Fix them first."
    exit 1
fi

# Start Aider for TDD
aider --model claude-3-5-sonnet-20241022 \
      --auto-commits \
      --message "test: TDD implementation"

echo "TDD session ready. Start with test cases."
EOF

# Usage: Write failing test first, then implement
> "Create a test for user registration that expects success"
> "Implement the user registration function to pass the test"
```

## Custom Commands and Macros

### Aider Command Extensions

```python
# Custom aider commands (experimental)
# Create aider command plugins
mkdir -p ~/.aider/commands

cat > ~/.aider/commands/git_status.py << 'EOF'
#!/usr/bin/env python3

import subprocess
import sys

def run_command(args):
    """Check git status before making changes."""
    result = subprocess.run(['git', 'status', '--porcelain'],
                          capture_output=True, text=True)

    if result.stdout.strip():
        print("Warning: You have uncommitted changes:")
        print(result.stdout)
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)

if __name__ == "__main__":
    run_command(sys.argv[1:])
EOF
```

### Workflow Templates

```bash
# Project templates
mkdir -p templates

# API endpoint template
cat > templates/api_endpoint.py << 'EOF'
@app.route('/api/{{endpoint}}', methods=['GET'])
def {{function_name}}():
    """
    {{endpoint_description}}
    """
    try:
        # Input validation
        # Business logic
        # Response formatting
        pass
    except Exception as e:
        # Error handling
        pass
EOF

# Usage with Aider
> "Create a new API endpoint for user profiles using the api_endpoint template"
```

## Repetitive Task Automation

### Code Generation Patterns

```bash
# Database model generation
> "Create SQLAlchemy models for User, Post, and Comment with proper relationships"

# API generation
> "Generate REST API endpoints for CRUD operations on the User model"

# Test generation
> "Create comprehensive unit tests for the authentication service"

# Documentation generation
> "Add docstrings and type hints to all functions in utils.py"
```

### Batch Operations

```bash
# Process multiple files
> /add src/**/*.py
> "Add logging statements to all public functions"

# Bulk refactoring
> "Convert all print statements to proper logging calls"

# Code standardization
> "Ensure all functions have type hints and docstrings"
```

## Integration Workflows

### Git Integration Workflows

```bash
# Feature branch workflow
cat > workflows/feature-workflow.sh << 'EOF'
#!/bin/bash
# Complete feature development workflow

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

# Setup
git checkout -b "$BRANCH_NAME"

# Development
aider --model claude-3-5-sonnet-20241022 \
      --auto-commits \
      --message "feat: Implement $FEATURE_NAME"

echo "Implement your feature. Press Ctrl+C when done."

# Testing
if command -v pytest &> /dev/null; then
    python -m pytest tests/ -v
fi

# Code review preparation
echo "Feature implementation complete."
echo "Run: git push -u origin $BRANCH_NAME"
echo "Then create a pull request for review."
EOF
```

### CI/CD Integration

```bash
# Automated code review workflow
cat > workflows/code-review.sh << 'EOF'
#!/bin/bash
# Automated code review workflow

echo "Running automated code review..."

# Start Aider for code review
aider --model claude-3-5-sonnet-20241022 \
      --no-auto-commits \
      --message "chore: Code review and improvements"

echo "Code review session ready."
echo "Commands:"
echo "  /add ."
echo "  > Review this code for security vulnerabilities"
echo "  > Check for performance issues"
echo "  > Ensure code follows best practices"
EOF
```

## Advanced Voice Features

### Voice Macros

```bash
# Create voice command shortcuts
cat > voice_macros.txt << 'EOF'
"add model" -> "Create a new SQLAlchemy model class"
"add test" -> "Create unit tests for the last function I implemented"
"refactor" -> "Refactor this code to improve readability and performance"
"document" -> "Add comprehensive docstrings to all functions"
"optimize" -> "Optimize this code for better performance"
EOF

# Voice macro usage
> "add model User with fields name, email, password"
# Expands to: "Create a new SQLAlchemy model class User with fields name, email, password"
```

### Voice Context Awareness

```bash
# Aider remembers voice context
> "Add error handling"

# Aider knows you're referring to the current function/file
# and adds appropriate error handling

# Continued conversation
> "Also add logging"
# Aider adds logging to the same context
```

### Multi-language Voice Support

```bash
# Voice works with any programming language
> "Create a React component for user login"

# Aider generates appropriate JavaScript/React code

> "Add CSS styling for the login form"

# Aider generates appropriate CSS
```

## Workflow Optimization

### Session Management

```bash
# Save and restore sessions
> /save-session my-feature-session

# Later restore
aider --restore-session my-feature-session

# Session includes:
# - Conversation history
# - File context
# - Model settings
# - Current state
```

### Batch Processing

```bash
# Process multiple related changes
cat > batch_changes.txt << 'EOF'
Add input validation to user registration
Add password strength checking
Add email format validation
Add rate limiting
Add security headers
EOF

# Process batch
while IFS= read -r change; do
    echo "Processing: $change"
    aider --model gpt-4o-mini --message "feat: $change" <<< "$change"
done < batch_changes.txt
```

### Template-Based Development

```bash
# Create project templates
mkdir -p templates/web-app
cat > templates/web-app/app.py << 'EOF'
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(debug=True)
EOF

# Use template
cp templates/web-app/app.py .
aider --message "feat: Initialize Flask application from template"
```

## Performance Workflows

### Code Optimization Workflows

```bash
# Performance optimization session
cat > workflows/optimize.sh << 'EOF'
#!/bin/bash
# Code optimization workflow

echo "Starting performance optimization..."

# Profile first
python -m cProfile -s time app.py > profile.txt

# Start optimization session
aider --model claude-3-5-sonnet-20241022 \
      --auto-commits \
      --message "perf: Performance optimizations"

echo "Optimization session ready."
echo "Review profile.txt and request optimizations."
EOF

# Usage
> "Optimize the database queries that are showing high execution time"
> "Add caching to frequently accessed functions"
> "Improve algorithm complexity in sorting functions"
```

### Memory Optimization

```bash
# Memory profiling workflow
pip install memory-profiler

cat > workflows/memory-profile.sh << 'EOF'
#!/bin/bash
# Memory profiling workflow

echo "Starting memory profiling..."

# Profile memory usage
python -m memory_profiler app.py

# Start optimization session
aider --model claude-3-5-sonnet-20241022 \
      --message "perf: Memory optimizations"

echo "Memory optimization session ready."
EOF
```

## Collaborative Workflows

### Team Development

```bash
# Shared configuration
cat > .aider.team.yml << 'EOF'
model: claude-3-5-sonnet-20241022
auto-commits: true
dark-mode: true
voice: true

# Team standards
code-style: pep8
documentation: google
testing: pytest
EOF

# Individual overrides
cat > .aider.personal.yml << 'EOF'
extends: .aider.team.yml
model: gpt-4o-mini  # Personal preference
EOF
```

### Code Review Workflows

```bash
# Automated code review
cat > workflows/review.sh << 'EOF'
#!/bin/bash
# Code review workflow

PR_NUMBER=$1

# Fetch PR changes
gh pr checkout $PR_NUMBER

# Start review session
aider --model claude-3-5-sonnet-20241022 \
      --no-auto-commits \
      --message "review: Code review for PR #$PR_NUMBER"

echo "Review session ready. Commands:"
echo "  /add ."
echo "  > Review for security vulnerabilities"
echo "  > Check code style and best practices"
echo "  > Suggest performance improvements"
EOF
```

## Summary

In this chapter, we've covered:

- **Voice Input**: Hands-free coding with speech recognition
- **Workflow Automation**: Scripts and templates for repetitive tasks
- **Custom Commands**: Extending Aider with personal commands
- **Batch Operations**: Processing multiple changes efficiently
- **Integration Workflows**: Git, CI/CD, and team collaboration
- **Performance Optimization**: Profiling and optimization workflows
- **Collaborative Development**: Team standards and code review processes

## Key Takeaways

1. **Voice Coding**: Enables hands-free development and accessibility
2. **Automation**: Create reusable workflows for common tasks
3. **Templates**: Use templates for consistent project structure
4. **Batch Processing**: Handle multiple changes efficiently
5. **Team Collaboration**: Establish shared workflows and standards
6. **Performance Focus**: Automated profiling and optimization
7. **Integration**: Connect Aider with existing development processes

## Next Steps

Now that you can automate workflows, let's explore **best practices** for effective AI pair programming.

---

**Ready for Chapter 8?** [Best Practices](08-best-practices.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*