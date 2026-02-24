---
layout: default
title: "Claude Code Tutorial - Chapter 2: Basic Commands"
nav_order: 2
has_children: false
parent: Claude Code Tutorial
---

# Chapter 2: Basic Commands - Essential Claude Code Operations

Welcome to **Chapter 2: Basic Commands - Essential Claude Code Operations**. In this part of **Claude Code Tutorial: Agentic Coding from Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master the core commands and operations for effective AI-powered terminal coding.

## Overview

This chapter covers the fundamental commands and operations in Claude Code. You'll learn how to navigate your codebase, run commands, manage files, and use Claude Code's core functionality effectively.

## Session Management

### Starting and Stopping Sessions

```bash
# Start interactive session
claude

# Start with specific project
cd my-project
claude

# Start with a specific task
claude "analyze the authentication code"

# Exit session
> /quit

# Or Ctrl+C (with confirmation)
```

### Session Commands

```bash
# Show help
> /help

# Output:
# Available commands:
# /help - Show this help message
# /clear - Clear conversation history
# /compact - Reduce context size to recent messages
# /cost - Show token usage and estimated cost
# /run <command> - Run a shell command
# /read <file> - Read and analyze a file
# /search <query> - Search codebase for text/patterns
# /quit - Exit Claude Code

# Clear conversation history
> /clear

# Compact context (keep recent messages)
> /compact

# Check costs
> /cost
# Session usage: 1,247 tokens ($0.03)
# Input: 892 tokens, Output: 355 tokens
```

## Codebase Navigation

### Project Analysis

```bash
# Get overview of project
> What does this project do?

# Claude analyzes:
# - package.json/README for project info
# - Main source files
# - Project structure
# - Technology stack

# Explore specific areas
> Show me the API routes
> Explain the database models
> What testing framework is used?
```

### File Operations

```bash
# Read specific files
> Read src/index.ts
> Show me the main configuration file
> What does the package.json contain?

# List directory contents
> What files are in the src directory?
> Show me the test files
> List all configuration files

# Find files by pattern
> Find all TypeScript files
> Show me files related to authentication
> What test files exist?
```

### Code Search

```bash
# Search for text patterns
> Search for "TODO" comments
> Find all console.log statements
> Search for "password" in the codebase

# Search with context
> Find functions that handle user login
> Search for database queries
> Find error handling code

# Advanced searches
> Find all API endpoints
> Search for security-related code
> Find deprecated functions
```

## File Editing

### Basic File Modifications

```bash
# Create new files
> Create a new file called utils/validation.ts with email validation functions

# Claude will:
# 1. Show the proposed file content
# 2. Ask for approval
# 3. Create the file
# 4. Show the diff

# Edit existing files
> Add error handling to the login function in auth.ts

# Claude will:
# 1. Read the current file
# 2. Propose changes
# 3. Show diff
# 4. Ask for approval
# 5. Apply changes
```

### Understanding Diffs

```bash
# Claude shows changes in unified diff format
# Example:
# --- a/src/auth.ts
# +++ b/src/auth.ts
# @@ -10,6 +10,10 @@ export async function login(email: string, password: string) {
#     const user = await findUserByEmail(email);
# +
# +   if (!user) {
# +     throw new Error('User not found');
# +   }
# +
#     const isValidPassword = await verifyPassword(password, user.passwordHash);
#
#     return { user, token: generateToken(user) };

# You can:
# - Approve with 'y'
# - Reject with 'n'
# - Request modifications
```

### Modifying Multiple Files

```bash
# Edit multiple files in one request
> Add logging to all API route handlers

# Claude will:
# 1. Find all relevant files
# 2. Show changes for each file
# 3. Apply changes file by file (with approval for each)

# Coordinated changes
> Rename the 'userId' field to 'user_id' across all model files

# Claude handles:
# - Finding all affected files
# - Making consistent changes
# - Maintaining references
```

## Command Execution

### Running Shell Commands

```bash
# Execute commands safely
> /run npm test

# Claude will:
# 1. Show the command to be executed
# 2. Ask for confirmation (for safety)
# 3. Execute the command
# 4. Show the output
# 5. Analyze results if relevant

# Common development commands
> /run npm install
> /run python -m pytest
> /run go test ./...
> /run docker build -t myapp .
```

### Command Sequences

```bash
# Run multiple commands
> First run the linter, then run the tests

# Claude will:
# 1. Execute: npm run lint
# 2. Show results
# 3. Then execute: npm test
# 4. Show results
# 5. Provide summary

# Build and deploy
> Build the application and run it locally

# Claude coordinates:
# 1. npm run build
# 2. npm start
# 3. Verify it's running
```

### Command Safety

```bash
# Safe command execution
> /run git status

# Dangerous commands get warnings
> /run rm -rf node_modules
# ⚠️  This command will delete files. Are you sure? [Y/n]

# Database commands get extra scrutiny
> /run rails db:migrate
# ⚠️  This will modify your database. Proceed? [Y/n]
```

## Git Integration

### Basic Git Operations

```bash
# Check repository status
> What changes are in the working directory?
> Show me the git status

# View recent commits
> What were the last 5 commits?
> Show me recent changes

# Create commits
# Claude automatically creates commits for file changes
# But you can also request specific commits
> Commit the current changes with message "Add user authentication"
```

### Git Workflow Integration

```bash
# Branch operations
> Create a new branch for the login feature
> Switch to the main branch

# Diff viewing
> Show me what changed in the last commit
> Compare the current branch with main

# Merge operations
> Merge the login feature branch into main
> Resolve any merge conflicts
```

### Commit Message Generation

```bash
# Claude generates meaningful commit messages
# Example changes:
> Add user registration API endpoint

# Generated commit:
# feat: Add user registration API endpoint with validation

# Complex changes:
> Implement password reset functionality with email notifications

# Generated commit:
# feat: Implement password reset with email notifications and token validation
```

## Code Analysis

### Code Understanding

```bash
# Analyze specific functions
> Explain what the authenticateUser function does
> Show me how the password hashing works

# Architecture analysis
> Describe the overall architecture of this application
> How do the different modules interact?

# Code quality assessment
> Are there any potential bugs in this code?
> What improvements could be made to this function?
```

### Dependency Analysis

```bash
# Package analysis
> What dependencies does this project use?
> Are there any outdated packages?

# Import analysis
> Show me the import structure
> Find unused imports
> Identify circular dependencies
```

### Security Analysis

```bash
# Security scanning
> Check for potential security vulnerabilities
> Look for hardcoded secrets
> Review authentication implementation

# Best practices
> Does this code follow security best practices?
> Are there any SQL injection risks?
> Check for proper input validation
```

## Testing Operations

### Running Tests

```bash
# Execute test suites
> Run the test suite
> Run only the unit tests
> Run tests for the authentication module

# Test results analysis
# Claude will:
# 1. Execute tests
# 2. Show output
# 3. Analyze failures
# 4. Suggest fixes
```

### Test Generation

```bash
# Generate tests
> Create unit tests for the user model
> Add integration tests for the API endpoints
> Generate tests for error conditions

# Test improvement
> The tests are failing, help me fix them
> Add more test coverage for edge cases
```

### Test Debugging

```bash
# Debug test failures
> The login test is failing, help me debug it
> Why is this test case not working?
> Fix the failing assertion in the test
```

## Error Handling

### Command Error Recovery

```bash
# Handle command failures
> The build is failing, help me fix it

# Claude will:
# 1. Analyze error output
# 2. Identify root cause
# 3. Suggest solutions
# 4. Apply fixes if approved

# Common error patterns:
# - Dependency issues
# - Syntax errors
# - Configuration problems
# - Missing files
```

### Code Error Resolution

```bash
# Fix compilation errors
> There are TypeScript errors, help me fix them
> The linter is complaining about unused variables

# Logic error debugging
> The login function isn't working correctly
> Users can't reset their passwords
> The API is returning 500 errors
```

## Performance Monitoring

### Session Performance

```bash
# Monitor token usage
> /cost

# Shows:
# - Total tokens used
# - Cost breakdown
# - Token efficiency

# Optimize usage
> /compact  # Reduce context size
> /clear    # Start fresh session
```

### Command Performance

```bash
# Time command execution
> Run the tests and show how long they take

# Claude will:
# 1. Time the command execution
# 2. Show performance metrics
# 3. Suggest optimizations if slow

# Performance analysis
> Why is the build taking so long?
> How can I speed up the test suite?
> Optimize this slow database query
```

## Workflow Patterns

### Development Workflow

```bash
# Feature development
1. > Create a new branch for the user profile feature
2. > Implement the user profile API endpoints
3. > Add validation and error handling
4. > Create tests for the new functionality
5. > Run the tests to make sure everything works
6. > Commit the changes with a descriptive message

# Bug fixing
1. > Analyze the reported bug in the login system
2. > Find the root cause of the issue
3. > Implement a fix for the bug
4. > Add a test case to prevent regression
5. > Verify the fix works correctly
```

### Code Review Workflow

```bash
# Code review assistance
> Review the changes in the last commit
> Check for security vulnerabilities
> Look for potential performance issues
> Ensure code follows project conventions

# Pull request assistance
> Prepare the pull request description
> Ensure all tests are passing
> Check that documentation is updated
> Verify the changes don't break existing functionality
```

### Refactoring Workflow

```bash
# Code refactoring
> Refactor the user authentication code to use dependency injection
> Split the large function into smaller, more focused functions
> Improve error handling throughout the application
> Add type annotations to improve code maintainability

# Architecture improvements
> Restructure the project to follow clean architecture principles
> Separate business logic from presentation logic
> Implement proper design patterns
> Improve testability of the codebase
```

## Summary

In this chapter, we've covered:

- **Session Management**: Starting, stopping, and managing Claude Code sessions
- **Codebase Navigation**: Analyzing projects, reading files, and searching code
- **File Editing**: Creating and modifying files with diff previews and approval
- **Command Execution**: Running shell commands safely with confirmation
- **Git Integration**: Working with version control and commit generation
- **Code Analysis**: Understanding code structure, dependencies, and security
- **Testing Operations**: Running tests, generating tests, and debugging failures
- **Error Handling**: Resolving command errors and code issues
- **Performance Monitoring**: Tracking usage and optimizing performance
- **Workflow Patterns**: Development, review, and refactoring workflows

## Key Takeaways

1. **Safety First**: All changes require approval, commands need confirmation
2. **Comprehensive Analysis**: Claude understands your entire codebase and tech stack
3. **Natural Interaction**: Communicate in plain English, Claude handles complexity
4. **Integrated Workflow**: Git, testing, and development tools work together
5. **Quality Focus**: Code analysis, security scanning, and best practices
6. **Performance Aware**: Cost tracking and context optimization
7. **Error Recovery**: Intelligent debugging and fix suggestions

## Next Steps

Now that you understand the basic commands, let's explore how Claude **understands your codebase** in depth.

---

**Ready for Chapter 3?** [Code Understanding](03-code-understanding.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Claude Code Tutorial: Agentic Coding from Your Terminal**
- tutorial slug: **claude-code-tutorial**
- chapter focus: **Chapter 2: Basic Commands - Essential Claude Code Operations**
- system context: **Claude Code Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 2: Basic Commands - Essential Claude Code Operations`.
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

1. Build a minimal end-to-end implementation for `Chapter 2: Basic Commands - Essential Claude Code Operations`.
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

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Show`, `files`, `changes` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Basic Commands - Essential Claude Code Operations` as an operating subsystem inside **Claude Code Tutorial: Agentic Coding from Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Claude`, `test`, `user` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Basic Commands - Essential Claude Code Operations` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Show`.
2. **Input normalization**: shape incoming data so `files` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `changes`.
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
- search upstream code for `Show` and `files` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Claude Code](01-getting-started.md)
- [Next Chapter: Chapter 3: Code Understanding - How Claude Analyzes Your Codebase](03-code-understanding.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
