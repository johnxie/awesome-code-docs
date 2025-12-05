---
layout: default
title: "Aider Tutorial - Chapter 5: Advanced Prompting"
nav_order: 5
has_children: false
parent: Aider Tutorial
---

# Chapter 5: Advanced Prompting

> Master advanced prompting techniques to get better results from AI, including context provision, specificity, and iterative refinement.

## Overview

The quality of your prompts directly affects the quality of Aider's responses. This chapter covers advanced prompting techniques to communicate effectively with AI and get the results you want.

## The Art of Clear Communication

### Be Specific About What You Want

```bash
# ❌ Vague
> Add error handling

# ✅ Specific
> Add try-catch blocks to the database connection methods in db.py that raise ConnectionError with descriptive messages when connections fail
```

### Provide Context

```bash
# ❌ No context
> Add validation

# ✅ With context
> Add input validation to the user registration API endpoint that checks email format using regex and password strength (minimum 8 characters, at least one uppercase, one lowercase, one number)
```

### Specify Implementation Details

```bash
# ❌ Implementation not specified
> Add caching

# ✅ Implementation specified
> Add Redis caching to the get_user_profile function with 5-minute TTL, using the redis-py library and connection pooling
```

## Understanding AI Capabilities and Limitations

### What AI Excels At

```bash
# AI is great at:
# - Code generation from specifications
# - Understanding patterns and conventions
# - Bug detection and fixing
# - Documentation writing
# - Refactoring and restructuring
# - Following established patterns

> Create a REST API endpoint for user management that follows REST conventions, includes proper HTTP status codes, and validates input data
```

### What Requires Human Guidance

```bash
# AI needs guidance for:
# - Business logic decisions
# - Performance vs simplicity trade-offs
# - Security considerations
# - Integration with existing systems

> Implement user authentication, but use JWT tokens instead of sessions, and ensure the tokens expire after 24 hours. Also, make sure to hash passwords with bcrypt before storing them.
```

## Prompt Engineering Techniques

### Step-by-Step Instructions

```bash
# Break complex tasks into steps
> Step 1: Create a User model class with fields for id, username, email, and password_hash
> Step 2: Add methods for password hashing and verification
> Step 3: Create a database migration for the users table
> Step 4: Add the model to the SQLAlchemy configuration
```

### Reference Existing Code

```bash
# Reference similar patterns in your codebase
> Create an Order model similar to the existing Product model, but with customer_id, total_amount, and status fields
```

### Specify Constraints and Requirements

```bash
# Be explicit about constraints
> Create a function to validate credit card numbers that:
> - Accepts Visa, MasterCard, and American Express
> - Uses the Luhn algorithm for validation
> - Returns a boolean and an error message
> - Does not store or log the card number anywhere
```

## Iterative Refinement

### Start Simple, Then Enhance

```bash
# First iteration: Basic functionality
> Create a simple function that sends an email

# Second iteration: Add features
> Add email templates and HTML support to the email function

# Third iteration: Add reliability
> Add retry logic and error handling to the email function
```

### Review and Improve

```bash
# After AI generates code
> /diff  # Review the changes

# Request improvements
> The error handling could be more specific. Catch SMTP-specific exceptions separately from network errors.

# Or ask for alternatives
> Instead of using smtplib directly, use a library like Flask-Mail for better integration with Flask applications
```

## Context Management

### Providing Sufficient Context

```bash
# Include relevant files
> /add models.py routes/auth.py

# Explain the current architecture
> We're using Flask with SQLAlchemy ORM and Flask-Login for session management. Add user registration functionality.
```

### Managing Conversation Context

```bash
# Aider remembers the conversation, so build upon previous work
> Add user login functionality that works with the registration system we just created

# Reference previous decisions
> Use the same password hashing approach we implemented in the User model
```

### Clearing Context When Needed

```bash
# Start fresh for unrelated tasks
> /clear

# Or be explicit about scope
> Create a new utility module for data processing that doesn't depend on the existing authentication code
```

## Pattern-Based Prompting

### Following Established Patterns

```bash
# Reference common patterns
> Implement the Repository pattern for data access, with separate repositories for User, Product, and Order entities

# Follow framework conventions
> Create a Django REST framework viewset for the User model with standard CRUD operations and proper serialization
```

### Code Style and Conventions

```bash
# Specify coding standards
> Write the code following PEP 8 style guidelines, with type hints, and comprehensive docstrings in Google style

# Follow project conventions
> Use the same logging and error handling patterns as the existing codebase in utils/logging.py
```

## Handling Complex Requirements

### Multi-Step Tasks

```bash
# Break down complex features
> Implement user authentication with the following components:
> 1. User model with password hashing
> 2. Registration endpoint with validation
> 3. Login endpoint with JWT token generation
> 4. Protected route decorator
> 5. Password reset via email
```

### Integration Requirements

```bash
# Specify integrations clearly
> Integrate with our existing PostgreSQL database using SQLAlchemy, and add proper indexes for the email and username fields
```

### Performance Considerations

```bash
# Include performance requirements
> Optimize the user search query with database indexes and implement caching with Redis for frequently accessed user profiles
```

## Error Handling and Debugging Prompts

### Anticipating Edge Cases

```bash
# Request comprehensive error handling
> Implement file upload functionality that handles large files, validates file types, prevents directory traversal attacks, and provides proper error messages for all failure cases
```

### Debugging Assistance

```bash
# Ask AI to help debug
> The user registration is failing with a database error. The error message is "UNIQUE constraint failed: users.email". Help me debug this issue.

# Or provide stack traces
> I'm getting this error when calling the API: [paste error]. The code is in api/users.py. What could be causing this?
```

## Security Considerations

### Secure Coding Practices

```bash
# Emphasize security
> Implement user authentication with secure password hashing using bcrypt, protection against timing attacks, and proper session management that includes secure cookie settings
```

### Input Validation

```bash
# Request thorough validation
> Add input sanitization and validation to the user profile update endpoint that prevents XSS attacks, validates email formats, and enforces length limits on all text fields
```

### Access Control

```bash
# Specify authorization requirements
> Implement role-based access control where admin users can manage all resources, regular users can only access their own data, and implement proper authorization checks in all API endpoints
```

## Testing and Quality Assurance

### Requesting Tests

```bash
# Ask for comprehensive testing
> Create unit tests for the user authentication functions, including tests for valid login, invalid credentials, password hashing, and edge cases like empty passwords
```

### Code Quality

```bash
# Request code reviews
> Review this authentication code for security vulnerabilities, performance issues, and adherence to best practices
```

## Working with Different Programming Paradigms

### Object-Oriented Programming

```bash
# Specify OOP patterns
> Refactor this procedural code into classes following the Single Responsibility Principle, with a UserService class for business logic and a UserRepository class for data access
```

### Functional Programming

```bash
# Request functional approaches
> Rewrite this imperative function using functional programming principles with pure functions, immutable data structures, and higher-order functions
```

### Asynchronous Programming

```bash
# Specify async patterns
> Convert these synchronous database operations to async using asyncio and async SQLAlchemy for better concurrency
```

## Framework-Specific Prompting

### Web Frameworks

```bash
# Django
> Create a Django model for User with proper field validations, model methods, and admin integration

# Flask
> Implement Flask blueprints for API routes with proper error handling and JSON responses

# Express.js
> Create Express middleware for authentication using JWT tokens with refresh token functionality
```

### Database Frameworks

```bash
# SQLAlchemy
> Create SQLAlchemy models with proper relationships, indexes, and constraints for a multi-tenant SaaS application

# Django ORM
> Design Django models with foreign keys, many-to-many relationships, and custom managers for complex querying
```

### Testing Frameworks

```bash
# pytest
> Write pytest test cases with fixtures, parametrization, and mocking for the authentication service

# Jest
> Create Jest tests for React components including user interactions, API calls, and error states
```

## Advanced Techniques

### Meta-Prompting

```bash
# Ask AI to improve your prompts
> I've been asking you to implement features, but the code quality could be better. What questions should I ask to get higher quality code?

# Or create templates
> Create a template for prompts when requesting new API endpoints that includes all the necessary details
```

### Chain of Thought

```bash
# Guide AI's reasoning
> To implement user notifications, I need to:
> 1. Define the notification data structure
> 2. Create a service to send notifications
> 3. Add database storage for notification history
> 4. Create API endpoints to manage notifications
> 5. Add real-time delivery mechanism
> Let's start with step 1
```

## Common Pitfalls and Solutions

### Overly Broad Requests

```bash
# ❌ Too broad
> Build a web application

# ✅ Focused
> Create a Flask route for user login with form validation and error handling
```

### Assuming Knowledge

```bash
# ❌ Assumes AI knows your setup
> Add logging

# ✅ Provides context
> Add structured logging using the logging library with JSON format, log levels, and rotation, similar to how it's done in utils/logging.py
```

### Incomplete Specifications

```bash
# ❌ Incomplete
> Create a user model

# ✅ Complete
> Create a SQLAlchemy User model with fields: id (primary key), username (unique, 80 chars), email (unique, 120 chars), password_hash (128 chars), created_at (datetime), is_active (boolean). Include methods for password hashing and verification.
```

## Summary

In this chapter, we've covered:

- **Clear Communication**: Being specific and providing context
- **Iterative Refinement**: Starting simple and improving incrementally
- **Context Management**: Managing conversation state and scope
- **Pattern-Based Prompting**: Following established conventions
- **Complex Requirements**: Breaking down multi-step tasks
- **Security and Quality**: Requesting secure, well-tested code
- **Framework-Specific**: Tailoring prompts to different technologies
- **Advanced Techniques**: Meta-prompting and chain of thought

## Key Takeaways

1. **Be Specific**: Clear, detailed prompts produce better results
2. **Provide Context**: Include relevant files and architectural information
3. **Iterate**: Start simple and refine through multiple interactions
4. **Follow Patterns**: Reference existing code and established conventions
5. **Break Down Tasks**: Divide complex work into manageable steps
6. **Specify Constraints**: Include security, performance, and quality requirements
7. **Review and Improve**: Always review changes and ask for improvements

## Next Steps

Now that you can prompt effectively, let's explore **model configuration** and how to choose the right AI model for different tasks.

---

**Ready for Chapter 6?** [Model Configuration](06-models.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*