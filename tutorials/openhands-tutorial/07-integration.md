---
layout: default
title: "OpenHands Tutorial - Chapter 7: Integration"
nav_order: 7
has_children: false
parent: OpenHands Tutorial
---

# Chapter 7: Integration - Connecting Applications with External Services

> Master OpenHands' integration capabilities for connecting applications with APIs, databases, third-party services, and complex system architectures.

## Overview

OpenHands excels at integrating applications with external services, APIs, and databases. This chapter covers comprehensive integration patterns, from simple API calls to complex distributed system orchestration.

## API Integration

### REST API Integration

```python
from openhands import OpenHands

# API integration agent
api_integrator = OpenHands()

# Complete REST API integration
rest_integration = api_integrator.run("""
Create comprehensive REST API integration for a weather application:

**External Weather API Integration:**
```python
# Current basic implementation
import requests

def get_weather(city):
    api_key = "your-api-key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity']
        }
    else:
        raise Exception(f"API call failed: {response.status_code}")
```

Enhance with:
1. **Request/Response Models** - Pydantic models for type safety
2. **Error Handling** - Comprehensive error handling and retry logic
3. **Rate Limiting** - Respect API rate limits with backoff strategies
4. **Caching** - Response caching to reduce API calls
5. **Authentication** - API key, OAuth, JWT token management
6. **Monitoring** - Request/response logging and metrics
7. **Fallback Mechanisms** - Alternative data sources when API fails
8. **Configuration Management** - Environment-based API configuration
9. **Testing** - Mock API responses for testing
10. **Documentation** - API usage documentation and examples

Include async support, circuit breaker patterns, and graceful degradation.
""")

# GraphQL API integration
graphql_integration = api_integrator.run("""
Implement GraphQL API integration with advanced features:

**GitHub GraphQL API Integration:**
```python
# Basic GraphQL query
def get_user_repos(username):
    query = '''
    query($username: String!) {
        user(login: $username) {
            repositories(first: 10) {
                nodes {
                    name
                    description
                    stargazerCount
                }
            }
        }
    }'''
    
    # Basic implementation
    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': {'username': username}},
        headers={'Authorization': f'bearer {token}'}
    )
    
    return response.json()
```

Enhance with:
1. **Query Builders** - Fluent API for constructing GraphQL queries
2. **Schema Introspection** - Dynamic query building from GraphQL schema
3. **Subscription Support** - Real-time data with GraphQL subscriptions
4. **Batch Operations** - Multiple queries in single request
5. **Fragment Management** - Reusable query fragments
6. **Type Safety** - Generated types from GraphQL schema
7. **Caching Strategy** - Intelligent caching based on query structure
8. **Error Handling** - Detailed GraphQL error parsing
9. **Testing** - Mock GraphQL server for testing
10. **Performance Optimization** - Query optimization and batching
""")

# Webhook and real-time integration
webhook_integration = api_integrator.run("""
Create webhook and real-time integration system:

**Stripe Payment Webhooks:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_json()
    
    # Basic webhook handling
    if payload['type'] == 'payment_intent.succeeded':
        payment_id = payload['data']['object']['id']
        # Process successful payment
        print(f"Payment {payment_id} succeeded")
    
    return jsonify({'status': 'ok'})
```

Enhance with:
1. **Webhook Verification** - Signature verification for security
2. **Event Processing** - Asynchronous event handling
3. **Retry Logic** - Failed webhook retry with exponential backoff
4. **Idempotency** - Prevent duplicate event processing
5. **Event Storage** - Persistent event logging and auditing
6. **Monitoring** - Webhook health and success rate monitoring
7. **Rate Limiting** - Protect against webhook spam
8. **Testing** - Webhook testing utilities and mock servers
9. **Documentation** - Webhook event documentation
10. **Multi-Provider Support** - Generic webhook handler for multiple providers
""")
```

## Database Integration

### Multiple Database Systems

```python
# Database integration agent
db_integrator = OpenHands()

# Comprehensive database integration
multi_db_integration = db_integrator.run("""
Create multi-database integration layer supporting different database systems:

**Supported Databases:**
1. PostgreSQL - Advanced relational features
2. MongoDB - Document-based NoSQL
3. Redis - In-memory data structure store
4. Elasticsearch - Full-text search and analytics

**Core Features:**
```python
# Current basic implementation
class DatabaseManager:
    def __init__(self, db_type, connection_string):
        if db_type == 'postgres':
            self.connection = psycopg2.connect(connection_string)
        elif db_type == 'mongodb':
            self.client = MongoClient(connection_string)
        # ... other databases
```

Enhance with:
1. **Unified Interface** - Common API across all database types
2. **Connection Pooling** - Efficient connection management
3. **Query Builders** - Type-safe query construction
4. **Migration System** - Database schema migrations
5. **Transaction Management** - ACID transaction support
6. **Caching Layer** - Multi-level caching (Redis + application cache)
7. **ORM Integration** - SQLAlchemy, MongoEngine, etc.
8. **Monitoring** - Query performance and connection monitoring
9. **Backup/Restore** - Automated backup and restore capabilities
10. **Security** - Encrypted connections and access control

Include database-specific optimizations, indexing strategies, and performance tuning.
""")

# Advanced database patterns
advanced_db_patterns = db_integrator.run("""
Implement advanced database integration patterns:

**CQRS (Command Query Responsibility Segregation):**
```python
class CQRSExample:
    def __init__(self):
        self.write_db = PostgreSQLConnection()  # For commands
        self.read_db = ElasticsearchConnection()  # For queries
    
    def create_user(self, user_data):
        # Command: Write to primary database
        user_id = self.write_db.insert('users', user_data)
        
        # Publish event for read model update
        self.publish_event('user_created', {'user_id': user_id, **user_data})
        
        return user_id
    
    def get_user_profile(self, user_id):
        # Query: Read from optimized read model
        return self.read_db.search('users', {'id': user_id})
```

**Event Sourcing:**
```python
class EventSourcingExample:
    def __init__(self):
        self.event_store = EventStore()
        self.projections = UserProjection()
    
    def update_user_email(self, user_id, new_email):
        # Store event instead of updating state directly
        event = {
            'type': 'user_email_updated',
            'user_id': user_id,
            'new_email': new_email,
            'timestamp': datetime.utcnow()
        }
        
        self.event_store.append(event)
        
        # Update read model
        self.projections.apply_event(event)
    
    def get_user(self, user_id):
        # Reconstruct state from events
        events = self.event_store.get_events(user_id)
        return self.projections.reconstruct_state(events)
```

**Database Sharding:**
```python
class ShardedDatabase:
    def __init__(self, shard_configs):
        self.shards = [DatabaseConnection(config) for config in shard_configs]
        self.shard_key = 'user_id'
    
    def get_shard(self, record):
        # Simple hash-based sharding
        shard_id = hash(record[self.shard_key]) % len(self.shards)
        return self.shards[shard_id]
    
    def insert(self, table, record):
        shard = self.get_shard(record)
        return shard.insert(table, record)
    
    def query(self, table, conditions):
        # Query all shards if no shard key in conditions
        if self.shard_key in conditions:
            shard = self.get_shard({self.shard_key: conditions[self.shard_key]})
            return shard.query(table, conditions)
        else:
            # Cross-shard query (more complex)
            results = []
            for shard in self.shards:
                results.extend(shard.query(table, conditions))
            return results
```

Include implementation details, trade-offs, and when to use each pattern.
""")
```

## Third-Party Service Integration

### Payment Processing

```python
# Payment integration agent
payment_integrator = OpenHands()

# Complete payment processing integration
payment_integration = payment_integrator.run("""
Create comprehensive payment processing integration:

**Supported Payment Providers:**
1. Stripe - Credit card processing
2. PayPal - PayPal payments
3. Square - Point of sale integration
4. Adyen - Global payment processing

**Core Features:**
```python
class PaymentProcessor:
    def __init__(self, provider='stripe'):
        self.provider = provider
        # Basic setup
    
    def process_payment(self, amount, currency, payment_method):
        # Basic payment processing
        pass
```

Enhance with:
1. **Unified Interface** - Common API across all payment providers
2. **Payment Methods** - Credit cards, digital wallets, bank transfers
3. **Security** - PCI compliance, tokenization, encryption
4. **Error Handling** - Payment failures, declines, chargebacks
5. **Webhooks** - Real-time payment status updates
6. **Refunds** - Partial and full refund processing
7. **Subscriptions** - Recurring payment management
8. **Fraud Detection** - Risk assessment and fraud prevention
9. **Multi-Currency** - International payment support
10. **Compliance** - Regulatory compliance (SOX, GDPR, etc.)

Include testing with mock payments, error simulation, and comprehensive logging.
""")

# Email and communication services
communication_integration = payment_integrator.run("""
Implement email and communication service integration:

**Email Providers:**
1. SendGrid - Transactional email
2. Mailgun - Email API service
3. Amazon SES - AWS email service
4. Postmark - Email delivery service

**Communication Features:**
```python
class EmailService:
    def send_email(self, to, subject, body):
        # Basic email sending
        pass
    
    def send_template_email(self, template_id, to, variables):
        # Template-based emails
        pass
```

Enhance with:
1. **Template Engine** - Dynamic email templates with variables
2. **Bulk Email** - Mass email campaigns with personalization
3. **Email Tracking** - Open rates, click tracking, bounces
4. **SMS Integration** - Twilio, AWS SNS for text messaging
5. **Push Notifications** - Firebase, OneSignal for mobile push
6. **Chat Integration** - Slack, Discord, Microsoft Teams
7. **Multi-Channel** - Unified messaging across channels
8. **Queue Management** - Asynchronous message processing
9. **Analytics** - Message delivery and engagement analytics
10. **Compliance** - CAN-SPAM, GDPR compliance for communications

Include A/B testing, personalization, and deliverability optimization.
""")

# Cloud service integration
cloud_integration = payment_integrator.run("""
Create cloud service integration layer:

**Cloud Providers:**
1. AWS - EC2, S3, Lambda, DynamoDB
2. Google Cloud - Compute Engine, Cloud Storage, Cloud Functions
3. Azure - VMs, Blob Storage, Functions, Cosmos DB

**Integration Patterns:**
```python
class CloudManager:
    def __init__(self, provider='aws'):
        self.provider = provider
    
    def upload_file(self, file_path, bucket):
        # File upload to cloud storage
        pass
    
    def run_function(self, function_name, payload):
        # Serverless function execution
        pass
```

Enhance with:
1. **Storage Integration** - File upload/download, CDN integration
2. **Compute Services** - Serverless functions, container orchestration
3. **Database Services** - Managed databases, caching layers
4. **AI/ML Services** - Pre-trained models, custom model hosting
5. **Monitoring** - Cloud-native monitoring and logging
6. **Security** - IAM, encryption, compliance certifications
7. **Cost Optimization** - Resource usage monitoring and optimization
8. **Multi-Cloud** - Unified interface across cloud providers
9. **Disaster Recovery** - Backup, failover, and recovery automation
10. **DevOps Integration** - CI/CD, infrastructure as code

Include provider-specific optimizations, cost monitoring, and migration strategies.
""")
```

## Message Queue and Event-Driven Integration

### Message Queue Systems

```python
# Message queue integration agent
queue_integrator = OpenHands()

# Complete message queue integration
message_queue_integration = queue_integrator.run("""
Implement comprehensive message queue integration:

**Supported Message Queues:**
1. RabbitMQ - Advanced message queuing
2. Apache Kafka - Distributed event streaming
3. Redis Queue - Simple in-memory queuing
4. Amazon SQS - AWS managed queue service

**Core Features:**
```python
class MessageQueue:
    def __init__(self, queue_type='rabbitmq'):
        self.queue_type = queue_type
    
    def publish_message(self, queue_name, message):
        # Publish message to queue
        pass
    
    def consume_messages(self, queue_name, callback):
        # Consume messages with callback
        pass
```

Enhance with:
1. **Message Serialization** - JSON, Avro, Protocol Buffers
2. **Reliability** - Message acknowledgments, dead letter queues
3. **Scalability** - Consumer group scaling, partition management
4. **Monitoring** - Queue depth, processing rates, error rates
5. **Security** - Message encryption, authentication, authorization
6. **Batching** - Message batching for efficiency
7. **Retry Logic** - Exponential backoff, circuit breakers
8. **Event Sourcing** - Event-driven architecture patterns
9. **Stream Processing** - Real-time data processing pipelines
10. **Integration Testing** - Message flow testing and validation

Include producer/consumer patterns, message routing, and error handling strategies.
""")

# Event-driven architecture
event_driven_integration = queue_integrator.run("""
Create event-driven architecture integration:

**Event Processing Patterns:**
```python
class EventProcessor:
    def __init__(self):
        self.event_handlers = {}
    
    def register_handler(self, event_type, handler):
        self.event_handlers[event_type] = handler
    
    def process_event(self, event):
        handler = self.event_handlers.get(event['type'])
        if handler:
            handler(event)
```

Enhance with:
1. **Event Sourcing** - Complete event history and replay
2. **CQRS Pattern** - Command Query Responsibility Segregation
3. **Saga Pattern** - Distributed transaction management
4. **Event Streaming** - Real-time event processing with Kafka
5. **Event Stores** - Persistent event storage and retrieval
6. **Event Versioning** - Schema evolution and compatibility
7. **Event Routing** - Content-based and header-based routing
8. **Monitoring** - Event throughput, latency, and error tracking
9. **Testing** - Event-driven test scenarios and mocking
10. **Documentation** - Event schema documentation and API

Include event schema definitions, event storming facilitation, and integration patterns.
""")
```

## Authentication and Authorization Integration

### OAuth and SSO Integration

```python
# Authentication integration agent
auth_integrator = OpenHands()

# Complete authentication system integration
auth_integration = auth_integrator.run("""
Create comprehensive authentication and authorization integration:

**Authentication Providers:**
1. Auth0 - Universal authentication platform
2. Firebase Auth - Google authentication service
3. AWS Cognito - AWS user identity management
4. Okta - Enterprise identity management

**Authorization Patterns:**
```python
class AuthManager:
    def __init__(self, provider='auth0'):
        self.provider = provider
    
    def authenticate_user(self, credentials):
        # User authentication
        pass
    
    def authorize_action(self, user, action, resource):
        # Action authorization
        pass
```

Enhance with:
1. **OAuth 2.0 Flows** - Authorization code, implicit, client credentials
2. **JWT Token Management** - Token generation, validation, refresh
3. **Role-Based Access Control** - User roles and permissions
4. **Multi-Factor Authentication** - SMS, TOTP, biometric factors
5. **Social Login** - Google, Facebook, GitHub authentication
6. **Single Sign-On** - Enterprise SSO integration
7. **Session Management** - Secure session handling and timeouts
8. **Audit Logging** - Authentication and authorization events
9. **Compliance** - GDPR, SOX, HIPAA compliance features
10. **Testing** - Authentication flow testing and mocking

Include security best practices, token security, and integration testing.
""")

# API gateway integration
api_gateway_integration = auth_integrator.run("""
Implement API gateway integration for service orchestration:

**API Gateway Features:**
```python
class APIGateway:
    def __init__(self):
        self.routes = {}
        self.middlewares = []
    
    def add_route(self, path, service, methods=['GET']):
        self.routes[path] = {'service': service, 'methods': methods}
    
    def handle_request(self, request):
        # Route request to appropriate service
        pass
```

Enhance with:
1. **Request Routing** - Path-based, header-based, and content-based routing
2. **Rate Limiting** - Request throttling and quota management
3. **Load Balancing** - Service instance distribution
4. **Authentication** - Centralized auth for all services
5. **Caching** - Response caching and cache invalidation
6. **Transformation** - Request/response transformation and adaptation
7. **Monitoring** - Request tracking, latency monitoring, error rates
8. **Security** - API key validation, CORS handling, security headers
9. **Documentation** - Auto-generated API documentation
10. **Testing** - Gateway testing and service mocking

Include service discovery, circuit breakers, and resilience patterns.
""")
```

## File and Media Integration

### Cloud Storage Integration

```python
# File integration agent
file_integrator = OpenHands()

# Complete file and media integration
file_integration = file_integrator.run("""
Create comprehensive file and media integration system:

**Storage Providers:**
1. Amazon S3 - Object storage service
2. Google Cloud Storage - Cloud storage platform
3. Azure Blob Storage - Microsoft's cloud storage
4. Cloudflare R2 - S3-compatible storage

**File Processing Features:**
```python
class FileManager:
    def __init__(self, provider='s3'):
        self.provider = provider
    
    def upload_file(self, file_path, destination):
        # File upload to cloud storage
        pass
    
    def download_file(self, source, local_path):
        # File download from cloud storage
        pass
```

Enhance with:
1. **File Upload/Download** - Resumable uploads, multipart uploads
2. **Media Processing** - Image resizing, video transcoding, format conversion
3. **CDN Integration** - Content delivery network for fast global access
4. **Security** - Signed URLs, access control, encryption
5. **Backup and Sync** - Automated backup, cross-region replication
6. **Metadata Management** - File metadata, tagging, search
7. **Versioning** - File version control and rollback
8. **Compression** - Automatic compression and optimization
9. **Virus Scanning** - Malware detection and prevention
10. **Analytics** - Usage statistics, access patterns, cost tracking

Include large file handling, streaming uploads/downloads, and integration testing.
""")

# Document processing integration
document_integration = file_integrator.run("""
Implement document processing and OCR integration:

**Document Processing Services:**
1. Google Document AI - Document understanding and OCR
2. AWS Textract - Document text extraction
3. Azure Form Recognizer - Form and document analysis
4. Adobe Document Services - PDF processing and manipulation

**Document Features:**
```python
class DocumentProcessor:
    def __init__(self, provider='google'):
        self.provider = provider
    
    def extract_text(self, document_path):
        # OCR text extraction
        pass
    
    def extract_form_data(self, form_path):
        # Form field extraction
        pass
```

Enhance with:
1. **OCR Processing** - Text extraction from images and PDFs
2. **Form Recognition** - Structured data extraction from forms
3. **Document Classification** - Automatic document type detection
4. **Table Extraction** - Table and spreadsheet data extraction
5. **Signature Detection** - Handwritten signature recognition
6. **Language Detection** - Multi-language document processing
7. **Quality Assessment** - OCR confidence scores and validation
8. **Batch Processing** - High-volume document processing
9. **Integration APIs** - REST APIs for document processing
10. **Workflow Automation** - Automated document processing pipelines

Include error handling, retry logic, and performance optimization.
""")
```

## Summary

In this chapter, we've covered OpenHands' comprehensive integration capabilities:

- **API Integration**: REST APIs, GraphQL, webhooks, real-time integration
- **Database Integration**: Multiple database systems, advanced patterns (CQRS, Event Sourcing)
- **Third-Party Services**: Payment processing, email/communication, cloud services
- **Message Queues**: Event-driven architecture, message processing patterns
- **Authentication**: OAuth, SSO, API gateways, authorization patterns
- **File/Media Integration**: Cloud storage, document processing, CDN integration

OpenHands can build complete, integrated systems that connect with external services, databases, and APIs while maintaining security, reliability, and performance.

## Key Takeaways

1. **Unified Interfaces**: Common APIs across different service providers
2. **Security First**: Secure authentication, encryption, and access control
3. **Reliability Patterns**: Circuit breakers, retries, fallback mechanisms
4. **Monitoring & Observability**: Comprehensive logging, metrics, and alerting
5. **Scalability**: Load balancing, caching, and performance optimization
6. **Testing Integration**: Mock services, integration testing, and validation

Next, we'll explore **advanced projects** - building complete applications, microservices, and complex system architectures.

---

**Ready for the next chapter?** [Chapter 8: Advanced Projects](08-advanced-projects.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*