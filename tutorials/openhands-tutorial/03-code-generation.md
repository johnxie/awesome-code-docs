---
layout: default
title: "OpenHands Tutorial - Chapter 3: Code Generation"
nav_order: 3
has_children: false
parent: OpenHands Tutorial
---

# Chapter 3: Code Generation - Creating Production-Ready Code

Welcome to **Chapter 3: Code Generation - Creating Production-Ready Code**. In this part of **OpenHands Tutorial: Autonomous Software Engineering Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master OpenHands' code generation capabilities for functions, classes, complete applications, and production-ready systems.

## Overview

OpenHands excels at generating high-quality, functional code from natural language descriptions. This chapter covers generating everything from simple functions to complex, multi-component applications with proper error handling, documentation, and testing.

## Function Generation

### Basic Function Creation

```python
from openhands import OpenHands

# Function generation agent
func_agent = OpenHands()

# Generate utility functions
utility_result = func_agent.run("""
Create a comprehensive string utility module with functions for:
1. Text cleaning and normalization
2. String validation and formatting
3. Text analysis and statistics
4. Encoding/decoding operations
5. String manipulation helpers

Include proper error handling, type hints, and comprehensive docstrings.
""")

# Generate mathematical functions
math_result = func_agent.run("""
Create a mathematical utilities module containing:
1. Statistical functions (mean, median, mode, std_dev)
2. Number theory functions (prime checking, factorial, gcd)
3. Matrix operations (addition, multiplication, transpose)
4. Numerical analysis (root finding, integration)
5. Random number generation utilities

Include input validation, edge case handling, and performance optimizations.
""")

# Generate data processing functions
data_result = func_agent.run("""
Create data processing utility functions for:
1. Data validation and cleaning
2. Format conversion (CSV, JSON, XML)
3. Data aggregation and grouping
4. Filtering and searching operations
5. Sorting and ordering functions
6. Duplicate detection and removal

Support multiple data types and include robust error handling.
""")
```

### Advanced Function Patterns

```python
# Generate higher-order functions
hof_result = func_agent.run("""
Create higher-order function utilities:
1. Function composition and piping
2. Memoization decorators
3. Retry and timeout decorators
4. Logging and profiling decorators
5. Validation decorators
6. Caching decorators

Include examples of usage for each pattern.
""")

# Generate async functions
async_result = func_agent.run("""
Create asynchronous utility functions for:
1. Concurrent API calls with rate limiting
2. File I/O operations with streaming
3. Database operations with connection pooling
4. Background task scheduling
5. Web scraping with concurrency control
6. Real-time data processing pipelines

Include proper async/await patterns and error handling.
""")

# Generate generator functions
generator_result = func_agent.run("""
Create generator function utilities for:
1. Lazy data processing pipelines
2. Memory-efficient file reading
3. Infinite sequences and series
4. Combinatorial generation
5. Stream processing operations
6. Pagination helpers

Include examples of memory-efficient data processing.
""")
```

## Class and Object Generation

### Basic Class Structures

```python
# Class generation agent
class_agent = OpenHands()

# Generate data model classes
model_result = class_agent.run("""
Create a complete data model hierarchy for an e-commerce system:
1. Base Entity class with common functionality
2. User model with authentication and profile management
3. Product model with inventory and pricing
4. Order model with payment processing
5. Category model with hierarchical relationships
6. Review model with rating and feedback

Include validation, serialization, and database integration methods.
""")

# Generate service classes
service_result = class_agent.run("""
Create service layer classes for the e-commerce system:
1. UserService for user management operations
2. ProductService for inventory management
3. OrderService for order processing and fulfillment
4. PaymentService for payment processing
5. EmailService for notifications
6. AnalyticsService for reporting and metrics

Include dependency injection, error handling, and logging.
""")

# Generate utility classes
utility_classes = class_agent.run("""
Create utility classes for common operations:
1. Configuration manager with environment variable handling
2. Logger class with multiple output formats
3. Cache manager with multiple storage backends
4. Validator class with extensible validation rules
5. FileManager for safe file operations
6. DateTime utilities with timezone support

Include singleton patterns where appropriate and comprehensive error handling.
""")
```

### Design Pattern Implementation

```python
# Design pattern generation
patterns_result = class_agent.run("""
Implement common design patterns as reusable classes:
1. Singleton pattern for resource management
2. Factory pattern for object creation
3. Observer pattern for event handling
4. Strategy pattern for algorithm selection
5. Decorator pattern for functionality extension
6. Command pattern for operation encapsulation

Provide concrete examples and usage demonstrations for each pattern.
""")

# Architectural pattern generation
architecture_result = class_agent.run("""
Create architectural pattern implementations:
1. MVC (Model-View-Controller) structure
2. Repository pattern for data access
3. Service layer pattern
4. Dependency injection container
5. Middleware pipeline for request processing
6. Event-driven architecture components

Include proper separation of concerns and extensibility features.
""")
```

## Complete Application Generation

### Web Application Frameworks

```python
# Web application generation
web_agent = OpenHands()

# FastAPI application
fastapi_result = web_agent.run("""
Create a complete FastAPI web application for a blog platform:
1. User authentication and authorization (JWT)
2. Blog post CRUD operations
3. Comment system with moderation
4. User profile management
5. File upload for images
6. API documentation with Swagger/OpenAPI
7. Database integration with SQLAlchemy
8. Background task processing
9. Comprehensive error handling
10. Input validation and serialization

Include proper project structure, requirements.txt, and deployment configuration.
""")

# Flask application
flask_result = web_agent.run("""
Build a Flask-based REST API for a task management system:
1. User registration and authentication
2. Task creation, updating, and deletion
3. Task assignment and status tracking
4. Project organization and categorization
5. Time tracking and reporting
6. Email notifications
7. Database models and migrations
8. API testing with pytest
9. Docker containerization
10. CI/CD pipeline configuration

Follow Flask best practices and include comprehensive documentation.
""")

# Django application
django_result = web_agent.run("""
Develop a Django application for an e-learning platform:
1. User roles (students, instructors, admins)
2. Course creation and management
3. Lesson content with multimedia support
4. Quiz and assessment system
5. Progress tracking and certificates
6. Discussion forums
7. Payment integration for premium courses
8. Admin interface customization
9. REST API with Django REST Framework
10. Comprehensive testing suite

Include proper Django project structure and deployment to production.
""")
```

### Data Science Applications

```python
# Data science application generation
ds_agent = OpenHands()

# Machine learning pipeline
ml_result = ds_agent.run("""
Create a complete machine learning pipeline for text classification:
1. Data ingestion and preprocessing
2. Feature extraction and engineering
3. Model training with multiple algorithms
4. Hyperparameter tuning and optimization
5. Model evaluation and validation
6. Model deployment and serving
7. Performance monitoring and logging
8. A/B testing framework
9. Retraining automation
10. API endpoint for predictions

Use scikit-learn, pandas, and FastAPI. Include proper error handling and documentation.
""")

# Data analysis dashboard
dashboard_result = ds_agent.run("""
Build a data analysis and visualization dashboard:
1. Data loading from multiple sources (CSV, database, API)
2. Data cleaning and preprocessing pipeline
3. Interactive charts and graphs with Plotly/Dash
4. Statistical analysis and summary statistics
5. Filtering and drill-down capabilities
6. Export functionality for reports
7. Real-time data updates
8. User authentication and access control
9. Responsive design for mobile and desktop
10. Performance optimization for large datasets

Include sample data and comprehensive documentation.
""")

# ETL pipeline
etl_result = ds_agent.run("""
Develop an ETL (Extract, Transform, Load) pipeline for data warehousing:
1. Data extraction from APIs, databases, and files
2. Data transformation and cleansing
3. Data validation and quality checks
4. Incremental loading with change detection
5. Error handling and recovery mechanisms
6. Monitoring and alerting
7. Configuration management
8. Testing framework for ETL operations
9. Documentation and lineage tracking
10. Performance optimization for large datasets

Use modern Python tools and best practices for data engineering.
""")
```

## Microservices and API Generation

### REST API Services

```python
# Microservice generation
micro_agent = OpenHands()

# User management microservice
user_service = micro_agent.run("""
Create a user management microservice with:
1. User registration and authentication
2. Profile management and preferences
3. Role-based access control
4. Password reset and security features
5. User activity logging
6. Integration with external identity providers
7. API rate limiting and throttling
8. Comprehensive API documentation
9. Health checks and monitoring endpoints
10. Docker containerization and deployment

Use FastAPI, PostgreSQL, and Redis for caching. Include proper testing and CI/CD.
""")

# Product catalog microservice
product_service = micro_agent.run("""
Build a product catalog microservice featuring:
1. Product CRUD operations
2. Category and taxonomy management
3. Inventory tracking and updates
4. Product search and filtering
5. Image upload and management
6. Pricing and discount management
7. Product reviews and ratings
8. Analytics and reporting
9. Bulk import/export operations
10. Event-driven architecture for updates

Include Elasticsearch for search, message queues for events, and comprehensive testing.
""")

# Order processing microservice
order_service = micro_agent.run("""
Develop an order processing microservice with:
1. Order creation and management
2. Payment processing integration
3. Inventory reservation and updates
4. Order status tracking and notifications
5. Refund and cancellation handling
6. Fraud detection and prevention
7. Multi-currency support
8. Tax calculation and compliance
9. Order analytics and reporting
10. Integration with shipping providers

Use event-driven architecture, saga pattern for distributed transactions, and comprehensive monitoring.
""")
```

### GraphQL APIs

```python
# GraphQL API generation
graphql_agent = OpenHands()

# GraphQL API with Strawberry
strawberry_result = graphql_agent.run("""
Create a GraphQL API for a social media platform using Strawberry:
1. User management with authentication
2. Post creation and interaction (likes, comments)
3. Follow/unfollow relationships
4. News feed with algorithmic ranking
5. Real-time subscriptions for updates
6. File upload for images and videos
7. Search functionality with Elasticsearch
8. Analytics and engagement metrics
9. Moderation and content filtering
10. Rate limiting and abuse prevention

Include proper schema design, resolvers, and comprehensive testing.
""")

# GraphQL federation
federation_result = graphql_agent.run("""
Implement a GraphQL federation architecture for a microservices platform:
1. Gateway service with Apollo Federation
2. User service subgraph
3. Product service subgraph
4. Order service subgraph
5. Review service subgraph
6. Schema stitching and composition
7. Cross-service data fetching
8. Entity extension and reference resolution
9. Authentication and authorization across services
10. Performance monitoring and optimization

Include proper service communication, error handling, and deployment configuration.
""")
```

## Code Quality and Best Practices

### Code Standards and Linting

```python
# Code quality agent
quality_agent = OpenHands()

# Code formatting and standards
standards_result = quality_agent.run("""
Implement comprehensive code quality standards:
1. Black code formatting configuration
2. Flake8 linting rules and plugins
3. MyPy type checking setup
4. Pre-commit hooks for quality gates
5. Editor configuration (VS Code, PyCharm)
6. CI/CD quality checks
7. Documentation standards (Google, NumPy style)
8. Code review checklist and guidelines
9. Automated code review tools
10. Quality metrics and reporting

Include configuration files and automation scripts.
""")

# Security best practices
security_result = quality_agent.run("""
Implement security best practices and tools:
1. Bandit security linting
2. Dependency vulnerability scanning
3. Secret management and detection
4. Input validation and sanitization
5. SQL injection prevention
6. XSS protection
7. CSRF protection
8. Rate limiting and abuse prevention
9. Security headers and HTTPS enforcement
10. Security monitoring and alerting

Include security testing frameworks and automated scanning.
""")
```

### Testing Framework Generation

```python
# Testing framework generation
test_agent = OpenHands()

# Unit testing setup
unit_tests = test_agent.run("""
Create a comprehensive unit testing framework:
1. pytest configuration and plugins
2. Test fixtures and factories
3. Mocking and patching utilities
4. Parameterized testing
5. Test coverage reporting
6. Test data management
7. Database testing utilities
8. API testing helpers
9. Performance testing utilities
10. Test automation and CI/CD integration

Include examples for different types of tests and best practices.
""")

# Integration testing
integration_tests = test_agent.run("""
Build integration testing capabilities:
1. End-to-end test scenarios
2. API integration testing
3. Database integration tests
4. External service mocking
5. Browser automation testing
6. Load and performance testing
7. Contract testing for microservices
8. Chaos engineering tests
9. Deployment verification tests
10. Monitoring and alerting integration

Include test data management and environment setup.
""")

# Property-based testing
property_tests = test_agent.run("""
Implement property-based testing with Hypothesis:
1. Property definitions for data structures
2. Invariant testing for algorithms
3. Edge case generation and testing
4. Stateful testing for complex systems
5. Integration with existing test suites
6. Test case minimization
7. Coverage-guided test generation
8. Performance regression testing
9. Fuzz testing integration
10. Test oracle development

Include examples and integration with CI/CD pipelines.
""")
```

## Documentation Generation

### API Documentation

```python
# Documentation generation
docs_agent = OpenHands()

# API documentation
api_docs = docs_agent.run("""
Generate comprehensive API documentation:
1. OpenAPI/Swagger specifications
2. Interactive API documentation
3. Code examples in multiple languages
4. Authentication documentation
5. Error handling documentation
6. Rate limiting documentation
7. SDK generation for different languages
8. Postman collection generation
9. API versioning documentation
10. Changelog and migration guides

Include proper formatting, examples, and usage instructions.
""")

# Code documentation
code_docs = docs_agent.run("""
Create comprehensive code documentation:
1. Docstring generation for all functions/classes
2. README files with installation and usage
3. Architecture documentation with diagrams
4. API reference documentation
5. Tutorial and getting started guides
6. Troubleshooting and FAQ sections
7. Contributing guidelines
8. Code of conduct and license information
9. Performance and scalability documentation
10. Security documentation and best practices

Use Sphinx or MkDocs for documentation generation and hosting.
""")
```

## Performance Optimization

### Optimized Code Generation

```python
# Performance optimization agent
perf_agent = OpenHands()

# Algorithm optimization
algorithm_opt = perf_agent.run("""
Create optimized algorithm implementations:
1. Efficient data structures (Bloom filters, Trie, etc.)
2. Optimized sorting and searching algorithms
3. Memory-efficient data processing
4. Concurrent and parallel processing
5. Caching strategies and implementations
6. Database query optimization
7. API rate limiting and throttling
8. Resource pooling and connection management
9. Lazy evaluation and streaming
10. Performance monitoring and profiling

Include benchmarks and performance comparisons.
""")

# System optimization
system_opt = perf_agent.run("""
Implement system-level optimizations:
1. Memory management and garbage collection
2. CPU cache optimization
3. I/O operation optimization
4. Network communication optimization
5. Database connection pooling
6. Background job processing
7. Caching layers (Redis, Memcached)
8. Load balancing strategies
9. Horizontal scaling patterns
10. Performance monitoring and alerting

Include configuration management and deployment considerations.
""")
```

## Multi-Language Code Generation

### Polyglot Applications

```python
# Multi-language code generation
polyglot_agent = OpenHands()

# Python backend with JavaScript frontend
fullstack_result = polyglot_agent.run("""
Create a full-stack application with Python backend and JavaScript frontend:
1. FastAPI backend with SQLAlchemy ORM
2. React frontend with TypeScript
3. RESTful API communication
4. JWT authentication
5. Real-time updates with WebSockets
6. File upload and management
7. Data visualization with charts
8. Responsive design with Tailwind CSS
9. Testing for both backend and frontend
10. Docker containerization for both services

Include proper project structure, dependency management, and deployment scripts.
""")

# Microservices with multiple languages
micro_polyglot = polyglot_agent.run("""
Build a microservices architecture with multiple languages:
1. API Gateway in Go for high performance
2. User service in Python with Django
3. Product service in Java with Spring Boot
4. Order service in Node.js with Express
5. Notification service in Rust for reliability
6. Analytics service in Scala with Akka
7. Service mesh with Istio
8. Event-driven communication with Kafka
9. Centralized logging and monitoring
10. CI/CD pipelines for each service

Include service discovery, circuit breakers, and distributed tracing.
""")
```

## Summary

In this chapter, we've explored OpenHands' comprehensive code generation capabilities:

- **Function Generation**: Utility functions, higher-order functions, async operations
- **Class and Object Generation**: Data models, service classes, design patterns
- **Complete Applications**: Web apps, data science projects, microservices
- **Code Quality**: Standards, security, testing frameworks
- **Documentation**: API docs, code documentation, tutorials
- **Performance**: Optimization techniques and system-level improvements
- **Multi-Language**: Polyglot applications and microservices

OpenHands can generate production-ready code across multiple domains and languages, with proper error handling, documentation, and testing.

## Key Takeaways

1. **Comprehensive Generation**: From simple functions to complex applications
2. **Production Quality**: Includes error handling, testing, and documentation
3. **Multi-Language Support**: Works across different programming languages
4. **Best Practices**: Follows industry standards and security practices
5. **Scalable Architecture**: Supports microservices and distributed systems

Next, we'll explore **bug fixing** - OpenHands' ability to identify, diagnose, and resolve code issues autonomously.

---

**Ready for the next chapter?** [Chapter 4: Bug Fixing](04-bug-fixing.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Include`, `testing`, `management` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Code Generation - Creating Production-Ready Code` as an operating subsystem inside **OpenHands Tutorial: Autonomous Software Engineering Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `generation`, `documentation`, `Create` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Code Generation - Creating Production-Ready Code` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Include`.
2. **Input normalization**: shape incoming data so `testing` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `management`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [OpenHands Repository](https://github.com/OpenHands/OpenHands)
  Why it matters: authoritative reference on `OpenHands Repository` (github.com).
- [OpenHands Docs](https://docs.openhands.dev/)
  Why it matters: authoritative reference on `OpenHands Docs` (docs.openhands.dev).
- [OpenHands Releases](https://github.com/OpenHands/OpenHands/releases)
  Why it matters: authoritative reference on `OpenHands Releases` (github.com).

Suggested trace strategy:
- search upstream code for `Include` and `testing` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Basic Operations - Files, Commands, and Environments](02-basic-operations.md)
- [Next Chapter: Chapter 4: Bug Fixing - Autonomous Debugging and Resolution](04-bug-fixing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
