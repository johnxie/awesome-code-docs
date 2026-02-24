---
layout: default
title: "Aider Tutorial - Chapter 5: Advanced Prompting"
nav_order: 5
has_children: false
parent: Aider Tutorial
---

# Chapter 5: Advanced Prompting

Welcome to **Chapter 5: Advanced Prompting**. In this part of **Aider Tutorial: AI Pair Programming in Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Aider Tutorial: AI Pair Programming in Your Terminal**
- tutorial slug: **aider-tutorial**
- chapter focus: **Chapter 5: Advanced Prompting**
- system context: **Aider Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 5: Advanced Prompting`.
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

1. Build a minimal end-to-end implementation for `Chapter 5: Advanced Prompting`.
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

### Scenario Playbook 1: Chapter 5: Advanced Prompting

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 5: Advanced Prompting

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 5: Advanced Prompting

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 5: Advanced Prompting

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 5: Advanced Prompting

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Create`, `user`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Advanced Prompting` as an operating subsystem inside **Aider Tutorial: AI Pair Programming in Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `email`, `model`, `using` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Advanced Prompting` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Create`.
2. **Input normalization**: shape incoming data so `user` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `error`.
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
- search upstream code for `Create` and `user` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Git Integration](04-git.md)
- [Next Chapter: Chapter 6: Model Configuration](06-models.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
