---
layout: default
title: "Aider Tutorial - Chapter 3: Multi-File Projects"
nav_order: 3
has_children: false
parent: Aider Tutorial
---

# Chapter 3: Multi-File Projects

Welcome to **Chapter 3: Multi-File Projects**. In this part of **Aider Tutorial: AI Pair Programming in Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Work across multiple files, manage complex codebases, and coordinate changes across your entire project.

## Overview

This chapter covers working with multi-file projects in Aider. You'll learn how to coordinate changes across multiple files, manage project structure, and handle complex refactoring that spans your entire codebase.

## Understanding Multi-File Context

### Repository Mapping

Aider uses a "repo-map" to understand your codebase structure:

```bash
$ aider
Aider v0.50.0
Models: claude-3-5-sonnet-20241022 with diff edit format
Git repo: .git with 47 files
Repo-map: using 2048 tokens  # Shows how much context is used
```

The repo-map helps Aider understand:
- File relationships and dependencies
- Project structure and organization
- Import patterns and module structure
- Code organization conventions

### Adding Multiple Files

```bash
# Add specific files
> /add src/main.py src/utils.py src/models.py

# Add entire directories
> /add src/ tests/

# Add with wildcards
> /add **/*.py

# Add files matching patterns
> /add src/**/*.py tests/test_*.py
```

## Coordinating Changes Across Files

### Example: Adding Authentication System

Let's build a complete authentication system across multiple files:

```bash
# Start in a Flask project
cd my-flask-app
aider

# Add all relevant files
> /add app.py models.py routes/auth.py templates/ utils/
```

**Request: Implement a complete user authentication system with registration, login, logout, and password reset**

Aider will create:
- User model in `models.py`
- Authentication routes in `routes/auth.py`
- Session management in `app.py`
- Password hashing utilities
- Email templates for password reset
- Database migrations if needed

### Managing File Dependencies

```python
# models.py - User model
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

```python
# routes/auth.py - Authentication routes
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))

        flash('Invalid username or password')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
```

```python
# app.py - Application setup
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')

# Import models after db is created
from models import User
```

## Cross-File Refactoring

### Example: Converting to Dependency Injection

```bash
# Original tightly coupled code
> /add service.py repository.py handlers/

# Request: Refactor the services to use dependency injection pattern

# Result across multiple files:

# service.py
class UserService:
    def __init__(self, user_repository, email_service):
        self.user_repository = user_repository
        self.email_service = email_service

    def create_user(self, username, email, password):
        user = self.user_repository.create(username, email, password)
        self.email_service.send_welcome_email(user.email)
        return user

# repository.py
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def create(self, username, email, password):
        # Database operations
        pass

# handlers/user_handler.py
def create_user_handler(request, user_service):
    data = request.get_json()
    user = user_service.create_user(
        data['username'],
        data['email'],
        data['password']
    )
    return {'user_id': user.id}, 201
```

## Managing Project Structure

### Creating New Files

```bash
# Request: Create a new API module with proper structure

# Aider creates:
# api/
# ├── __init__.py
# ├── routes.py
# ├── schemas.py
# └── middleware.py
```

### Restructuring Existing Code

```bash
# Original: Everything in one file
> /add monolithic.py

# Request: Split this monolithic file into proper modules

# Result: Creates multiple files
# models/
# ├── user.py
# ├── product.py
# └── order.py
# services/
# ├── user_service.py
# ├── product_service.py
# └── order_service.py
# api/
# ├── user_routes.py
# ├── product_routes.py
# └── order_routes.py
```

## Working with Tests

### Adding Tests for New Features

```bash
# After implementing a feature
> /add tests/

# Request: Create comprehensive unit tests for the authentication system

# Aider creates:
# tests/
# ├── test_auth.py
# ├── test_models.py
# ├── test_routes.py
# ├── conftest.py
# └── fixtures/
#     └── users.py
```

### Test-Driven Development

```bash
# Request: Implement a shopping cart feature with tests first

# Aider creates:
# tests/test_cart.py
# models/cart.py
# services/cart_service.py
# routes/cart.py
```

## Configuration Management

### Environment-Specific Configs

```bash
# Request: Create environment-specific configuration files

# Aider creates:
# config/
# ├── default.py
# ├── development.py
# ├── testing.py
# └── production.py
#
# .env.example
# docker-compose.yml
```

### Managing Secrets

```bash
# Request: Implement secure configuration management

# Aider creates:
# config/secrets.py (with warnings about security)
# .env.local (gitignored)
# docker/secrets/
# ├── db_password.txt
# └── api_key.txt
```

## Database Operations

### Schema Migrations

```bash
# Request: Create database migration for user authentication tables

# Aider creates:
# migrations/
# ├── 001_create_users_table.sql
# ├── 002_add_user_roles.sql
# └── 003_create_sessions_table
#
# models/user.py (updated)
# models/role.py (new)
```

### ORM Integration

```bash
# Request: Convert raw SQL to SQLAlchemy ORM models

# Result: Proper ORM models with relationships
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="users")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
```

## API Development

### REST API Implementation

```bash
# Request: Create a REST API for user management

# Aider creates:
# api/
# ├── users.py
# ├── middleware.py
# └── schemas.py
#
# tests/
# ├── test_users_api.py
# └── test_schemas.py
```

### GraphQL API

```bash
# Request: Implement GraphQL API for the application

# Aider creates:
# graphql/
# ├── schema.py
# ├── types.py
# ├── resolvers.py
# └── mutations.py
#
# api/graphql.py
```

## Frontend Integration

### Template Management

```bash
# Request: Create HTML templates for the authentication system

# Aider creates:
# templates/
# ├── base.html
# ├── login.html
# ├── register.html
# ├── profile.html
# └── errors/
#     └── 404.html
```

### Static Assets

```bash
# Request: Add CSS and JavaScript for the user interface

# Aider creates:
# static/
# ├── css/
# │   ├── main.css
# │   └── auth.css
# ├── js/
# │   ├── app.js
# │   └── auth.js
# └── images/
#     └── logo.png
```

## Deployment Configuration

### Docker Setup

```bash
# Request: Create Docker configuration for the application

# Aider creates:
# Dockerfile
# docker-compose.yml
# .dockerignore
# docker/
# ├── Dockerfile.prod
# └── nginx.conf
```

### Kubernetes Manifests

```bash
# Request: Create Kubernetes deployment manifests

# Aider creates:
# k8s/
# ├── deployment.yaml
# ├── service.yaml
# ├── configmap.yaml
# ├── secret.yaml
# └── ingress.yaml
```

## Best Practices for Multi-File Projects

### Plan Before Implementing

```bash
# Think about the overall architecture first
> I want to build a blog application. First, help me design the overall structure with models, views, and APIs.

# Then implement incrementally
> Start with the User model and authentication
> Then add the Post model and CRUD operations
> Finally add comments and relationships
```

### Use Clear Separation of Concerns

```bash
# Request: Refactor this code to follow clean architecture principles

# Aider will create:
# - Clear separation between business logic, data access, and presentation
# - Dependency injection for testability
# - Interface definitions for loose coupling
```

### Maintain Consistency

```bash
# Request: Ensure all files follow the same naming conventions and patterns

# Aider will:
# - Standardize variable naming
# - Apply consistent code formatting
# - Use uniform error handling patterns
```

### Document as You Go

```bash
# Request: Add comprehensive documentation for the entire codebase

# Aider creates:
# - README.md files for each module
# - Inline documentation for all functions
# - API documentation
# - Architecture diagrams (in comments)
```

## Troubleshooting Multi-File Issues

### Dependency Resolution

```bash
# If Aider suggests circular imports
> Refactor to break the circular dependency between module A and module B

# Aider will suggest:
# - Extract common interfaces
# - Use dependency injection
# - Reorganize module structure
```

### File Conflicts

```bash
# If changes conflict between files
> /diff  # Review all changes
> These changes to file A and file B conflict. Please resolve the conflict.

# Aider will help coordinate the changes
```

### Large Codebases

```bash
# For very large projects, be specific about scope
> Only modify the authentication-related files, don't touch the payment system

# Use targeted file selection
> /add auth/ models/user.py  # Only these files
```

## Summary

In this chapter, we've covered:

- **Multi-File Context**: Understanding repository mapping and file relationships
- **Coordinated Changes**: Implementing features across multiple files
- **Project Structure**: Creating and managing complex project layouts
- **Cross-File Refactoring**: Restructuring code across the entire codebase
- **Testing**: Adding comprehensive tests for multi-file features
- **Configuration**: Managing environment-specific and secure configurations
- **Database Operations**: Schema migrations and ORM integration
- **API Development**: REST and GraphQL API implementation
- **Frontend Integration**: Templates and static assets
- **Deployment**: Docker and Kubernetes configuration

## Key Takeaways

1. **Plan Architecture**: Design overall structure before implementation
2. **Incremental Development**: Build features step by step across files
3. **Consistent Patterns**: Maintain uniform conventions across all files
4. **Dependency Management**: Handle imports and relationships carefully
5. **Testing Coverage**: Add tests for all multi-file interactions
6. **Documentation**: Document as you develop for maintainability

## Next Steps

Now that you can work across multiple files, let's explore **Git integration** and how Aider manages version control automatically.

---

**Ready for Chapter 4?** [Git Integration](04-git.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Aider Tutorial: AI Pair Programming in Your Terminal**
- tutorial slug: **aider-tutorial**
- chapter focus: **Chapter 3: Multi-File Projects**
- system context: **Aider Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Multi-File Projects`.
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

1. Build a minimal end-to-end implementation for `Chapter 3: Multi-File Projects`.
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

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Aider`, `user`, `Request` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Multi-File Projects` as an operating subsystem inside **Aider Tutorial: AI Pair Programming in Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `models`, `username`, `self` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Multi-File Projects` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Aider`.
2. **Input normalization**: shape incoming data so `user` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Request`.
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
- search upstream code for `Aider` and `user` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Basic Editing Operations](02-basic-editing.md)
- [Next Chapter: Chapter 4: Git Integration](04-git.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
