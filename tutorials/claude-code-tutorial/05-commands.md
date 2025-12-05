---
layout: default
title: "Claude Code Tutorial - Chapter 5: Command Execution"
nav_order: 5
has_children: false
parent: Claude Code Tutorial
---

# Chapter 5: Command Execution - Running Tests, Builds, and Scripts

> Master safe command execution, test running, build processes, and development workflow automation.

## Overview

Claude Code can execute shell commands safely, allowing you to run tests, builds, deployments, and other development tasks. This chapter covers command execution patterns, safety measures, and integration with development workflows.

## Basic Command Execution

### Safe Command Running

```bash
# Execute commands with safety checks
> /run npm test

# Claude will:
# 1. Show the command to be executed
# 2. Check for potentially dangerous operations
# 3. Ask for confirmation if risky
# 4. Execute the command
# 5. Show output and analyze results

# Example interaction:
# I'm about to run: npm test
# This will execute your test suite. Proceed? [Y/n] y
#
# Running npm test...
# > myapp@1.0.0 test
# > jest
#
# PASS src/utils.test.js
# PASS src/api.test.js
# Test Suites: 2 passed, 2 total
# Tests: 15 passed, 15 total
#
# Tests completed successfully!
```

### Command Categories

```bash
# Safe commands (no confirmation needed):
> /run git status
> /run ls -la
> /run cat README.md
> /run pwd

# Development commands:
> /run npm install
> /run python -m pytest
> /run go test ./...
> /run ./gradlew build

# Risky commands (require confirmation):
> /run rm -rf node_modules
> /run git reset --hard
> /run rails db:migrate
> /run docker system prune
```

## Testing Operations

### Running Test Suites

```bash
# Run all tests
> Run the test suite

# Claude executes appropriate test command based on project:
# - npm test (JavaScript/Node.js)
# - python -m pytest (Python)
# - go test (Go)
# - ./gradlew test (Java/Gradle)
# - mvn test (Java/Maven)

# Run specific test files
> Run tests for the authentication module
> Run the user model tests
> Run integration tests only
```

### Test Analysis and Fixes

```bash
# Analyze test failures
> The tests are failing, help me debug this

# Claude will:
# 1. Run the tests to see failures
# 2. Analyze error messages
# 3. Identify root causes
# 4. Suggest fixes
# 5. Apply fixes if approved

# Example test debugging:
> 2 tests failed in src/auth.test.js
#
# FAIL src/auth.test.js
#   ● Login validation
#     Expected password validation to reject short passwords
#
#   ● Password hashing
#     Expected bcrypt to hash passwords properly
#
# Root cause: Password validation logic is incorrect.
# The minimum length check is using >= instead of >.
#
# Would you like me to fix this?
```

### Test Generation

```bash
# Generate tests for new code
> Create unit tests for the new user registration function

# Claude will:
# 1. Analyze the function
# 2. Generate comprehensive test cases
# 3. Include edge cases and error conditions
# 4. Follow project testing conventions

# Example generated test:
def test_user_registration():
    # Test successful registration
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }

    user = register_user(user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash is not None

    # Test validation errors
    with pytest.raises(ValueError):
        register_user({"username": "", "email": "invalid", "password": "short"})

    # Test duplicate email
    with pytest.raises(ValueError):
        register_user(user_data)  # Same email
```

## Build and Deployment

### Build Processes

```bash
# Run build commands
> Build the application

# Claude executes appropriate build command:
# - npm run build (frontend)
# - python setup.py build (Python)
# - go build (Go)
# - ./gradlew build (Gradle)
# - mvn package (Maven)

# Build with specific options
> Build in production mode
> Build with optimizations
> Create release build
```

### Deployment Operations

```bash
# Safe deployment commands
> Deploy to staging environment

# Claude will:
# 1. Build the application
# 2. Run pre-deployment checks
# 3. Execute deployment script
# 4. Verify deployment success
# 5. Run post-deployment tests

# Rollback capability
> Rollback the last deployment

# Claude handles rollback procedures
```

### Container Operations

```bash
# Docker commands (with safety checks)
> Build the Docker image
> Start the development containers
> Run database migrations in container

# Example Docker workflow:
> /run docker-compose up -d db
# Starting database container...
# Database is ready.

> /run docker-compose run --rm app python manage.py migrate
# Running migrations...
# Migrations completed successfully.
```

## Development Workflow Automation

### Code Quality Checks

```bash
# Run linting and formatting
> Run the linter
> Format the code
> Check code quality

# Claude executes:
# - ESLint/Prettier (JavaScript)
# - flake8/black (Python)
# - golint/gofmt (Go)
# - Checkstyle (Java)

# Fix identified issues
> Fix the linting errors
> Format all files
> Resolve code quality issues
```

### Dependency Management

```bash
# Package management
> Install dependencies
> Update dependencies safely
> Check for security vulnerabilities

# Example dependency workflow:
> /run npm audit
# Found 3 vulnerabilities, 2 moderate, 1 high severity.
#
# Would you like me to fix these vulnerabilities?

> Yes, update the vulnerable packages

# Claude will:
# 1. Identify safe updates
# 2. Update package versions
# 3. Run tests to ensure compatibility
# 4. Commit changes if successful
```

### Git Operations

```bash
# Git workflow integration
> Commit the current changes
> Create a new branch for the feature
> Push changes to remote
> Create a pull request

# Example Git workflow:
> Create a feature branch for user authentication

# Claude will:
# 1. Check current branch
# 2. Create new branch
# 3. Switch to new branch
# 4. Confirm success

# Commit with generated message:
> /run git add .
> /run git commit -m "feat: Implement user authentication system"
```

## Advanced Command Patterns

### Multi-Command Sequences

```bash
# Execute command chains
> First run the tests, then build the application if tests pass

# Claude will:
# 1. Run tests
# 2. Check test results
# 3. Only build if tests pass
# 4. Report overall status

# Conditional execution
> If tests pass, deploy to staging

# Error handling in sequences
> Run linter, fix any auto-fixable issues, then run tests
```

### Background Processes

```bash
# Start background services
> Start the development server in background

# Claude will:
# 1. Start the server process
# 2. Detach from terminal
# 3. Confirm it's running
# 4. Provide process information

# Monitor background processes
> Check if the server is running
> Show server logs
> Restart the server if needed
```

### Command Templates

```bash
# Reuse command patterns
> Run the standard CI pipeline locally

# Claude remembers and executes:
# 1. Install dependencies
# 2. Run linter
# 3. Run tests
# 4. Build application
# 5. Run integration tests

# Custom command templates
> Run the performance test suite
> Execute the security scan
> Run the deployment checklist
```

## Safety and Security

### Command Validation

```bash
# Dangerous command detection
> /run rm -rf /

# Claude will block:
# ⚠️  This command is potentially destructive.
# It will delete all files on the system.
# This action is not allowed.

# Safe alternatives suggested:
> /run rm -rf build/
> /run rm -rf node_modules/
```

### Permission Checks

```bash
# File system permissions
> /run chmod 755 scripts/deploy.sh

# Claude checks:
# - File exists
# - User has permissions
# - Command is safe

# Network operations
> /run curl https://api.example.com/data

# Claude validates:
# - URL is safe
# - No sensitive data in command
# - Network access is allowed
```

### Audit Logging

```bash
# Command execution logging
# Claude logs all commands executed:
# - Timestamp
# - Command executed
# - User confirmation status
# - Success/failure status
# - Output summary

# View command history
> Show recent command executions

# Audit trail for compliance
> Export command execution log
```

## Error Handling and Recovery

### Command Failure Analysis

```bash
# Analyze failed commands
> The build failed, help me debug this

# Claude will:
# 1. Show the full error output
# 2. Identify the error type
# 3. Suggest solutions
# 4. Offer to apply fixes

# Example build failure:
# ERROR: Module 'requests' not found
#
# Solutions:
# 1. Install missing dependency: pip install requests
# 2. Add to requirements.txt
# 3. Check Python path
#
# Would you like me to install the missing dependency?
```

### Recovery Procedures

```bash
# Automatic recovery attempts
> The tests are failing due to database connection

# Claude tries:
# 1. Check if database is running
# 2. Restart database if needed
# 3. Re-run tests
# 4. Report results

# Manual recovery guidance
> How do I fix this Docker networking issue?

# Claude provides step-by-step recovery:
# 1. Stop containers: docker-compose down
# 2. Remove networks: docker network prune
# 3. Restart containers: docker-compose up -d
# 4. Verify connectivity: docker exec app ping db
```

### Rollback Procedures

```bash
# Rollback failed operations
> The deployment failed, rollback to previous version

# Claude will:
# 1. Identify rollback strategy
# 2. Execute rollback commands
# 3. Verify system stability
# 4. Report rollback status

# Database rollbacks
> Rollback the failed database migration

# Code rollbacks
> Revert the last commit that broke the build
```

## Performance Monitoring

### Command Performance Tracking

```bash
# Monitor command execution time
> /run time npm test

# Claude tracks:
# - Command execution time
# - Resource usage
# - Success/failure rates
# - Performance trends

# Performance analysis
> Why is the build taking so long?

# Claude analyzes:
# - Build steps timing
# - Bottleneck identification
# - Optimization suggestions
```

### Resource Usage Monitoring

```bash
# Monitor system resources during commands
> Run the test suite and monitor resource usage

# Claude reports:
# - CPU usage during execution
# - Memory consumption
# - Disk I/O patterns
# - Network activity

# Resource optimization
> The tests are using too much memory, help optimize

# Suggestions:
# - Reduce test parallelism
# - Use in-memory databases for tests
# - Implement test data cleanup
```

## Integration Patterns

### CI/CD Integration

```bash
# Simulate CI/CD pipelines
> Run the full CI pipeline locally

# Claude executes:
# 1. Checkout code
# 2. Install dependencies
# 3. Run linting
# 4. Run tests
# 5. Build application
# 6. Run security scans
# 7. Create artifacts

# CI debugging
> The CI build is failing, help me reproduce locally

# Claude helps:
# 1. Reproduce CI environment
# 2. Run same commands locally
# 3. Debug the failure
# 4. Suggest fixes
```

### IDE Integration

```bash
# Work with various editors
> Open the failing test in VS Code
> Show the error location in the editor
> Open the project in the configured editor

# Editor commands:
# - code <file> (VS Code)
# - atom <file> (Atom)
# - sublime <file> (Sublime Text)
# - vim <file> (Vim)
```

### Team Workflow Integration

```bash
# Standardized team commands
> Run the team code quality checks

# Claude executes team standards:
# 1. Run linter with team config
# 2. Check commit message format
# 3. Run security scans
# 4. Validate documentation

# Onboarding automation
> Set up the development environment

# Claude configures:
# 1. Install dependencies
# 2. Set up pre-commit hooks
# 3. Configure IDE settings
# 4. Run initial tests
```

## Summary

In this chapter, we've covered:

- **Basic Command Execution**: Safe command running with approval workflow
- **Testing Operations**: Running tests, analyzing failures, generating tests
- **Build and Deployment**: Building applications and managing deployments
- **Development Workflows**: Code quality, dependencies, Git operations
- **Advanced Patterns**: Multi-command sequences, background processes, templates
- **Safety and Security**: Command validation, permissions, audit logging
- **Error Handling**: Failure analysis, recovery procedures, rollbacks
- **Performance Monitoring**: Execution tracking and resource optimization
- **Integration Patterns**: CI/CD, IDE, and team workflow integration

## Key Takeaways

1. **Safety First**: All commands require confirmation, especially destructive ones
2. **Intelligent Analysis**: Claude understands command outputs and suggests fixes
3. **Workflow Automation**: Complex development tasks can be automated
4. **Error Recovery**: Comprehensive debugging and recovery capabilities
5. **Performance Aware**: Monitors and optimizes command execution
6. **Integration Ready**: Works with existing development tools and processes
7. **Audit Trail**: Complete logging of all command executions
8. **Team Collaboration**: Supports standardized team workflows

## Next Steps

Now that you can execute commands effectively, let's explore **Git workflows** and version control integration in detail.

---

**Ready for Chapter 6?** [Git Workflows](06-git.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*