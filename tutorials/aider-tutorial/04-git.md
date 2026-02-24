---
layout: default
title: "Aider Tutorial - Chapter 4: Git Integration"
nav_order: 4
has_children: false
parent: Aider Tutorial
---

# Chapter 4: Git Integration

Welcome to **Chapter 4: Git Integration**. In this part of **Aider Tutorial: AI Pair Programming in Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Aider Tutorial: AI Pair Programming in Your Terminal**
- tutorial slug: **aider-tutorial**
- chapter focus: **Chapter 4: Git Integration**
- system context: **Aider Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 4: Git Integration`.
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

- [Aider Repository](https://github.com/Aider-AI/aider)
- [Aider Releases](https://github.com/Aider-AI/aider/releases)
- [Aider Docs](https://aider.chat/)

### Cross-Tutorial Connection Map

- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Continue Tutorial](../continue-tutorial/)
- [Codex Analysis Platform](../codex-analysis-platform/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 4: Git Integration`.
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

### Scenario Playbook 1: Chapter 4: Git Integration

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 4: Git Integration

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `auto`, `commits`, `Aider` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Git Integration` as an operating subsystem inside **Aider Tutorial: AI Pair Programming in Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Commit`, `aider`, `feat` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Git Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `auto`.
2. **Input normalization**: shape incoming data so `commits` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Aider`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Aider Repository](https://github.com/Aider-AI/aider)
  Why it matters: authoritative reference on `Aider Repository` (github.com).
- [Aider Releases](https://github.com/Aider-AI/aider/releases)
  Why it matters: authoritative reference on `Aider Releases` (github.com).
- [Aider Docs](https://aider.chat/)
  Why it matters: authoritative reference on `Aider Docs` (aider.chat).

Suggested trace strategy:
- search upstream code for `auto` and `commits` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Multi-File Projects](03-multi-file.md)
- [Next Chapter: Chapter 5: Advanced Prompting](05-prompting.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
