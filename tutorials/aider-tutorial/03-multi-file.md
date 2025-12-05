---
layout: default
title: "Aider Tutorial - Chapter 3: Multi-File Projects"
nav_order: 3
has_children: false
parent: Aider Tutorial
---

# Chapter 3: Multi-File Projects

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