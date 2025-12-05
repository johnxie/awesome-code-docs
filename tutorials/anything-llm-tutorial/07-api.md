---
layout: default
title: "AnythingLLM Tutorial - Chapter 7: API & Integration"
nav_order: 7
has_children: false
parent: AnythingLLM Tutorial
---

# Chapter 7: API & Integration - Programmatic Access and System Integration

> Integrate AnythingLLM into your applications with comprehensive API access and automation capabilities.

## Overview

AnythingLLM provides a full REST API for programmatic access to all features. This chapter covers API usage, integration patterns, and building applications that leverage AnythingLLM's capabilities.

## API Fundamentals

### Authentication

```bash
# Create API key
curl -X POST http://localhost:3001/api/v1/auth/api-key \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Application",
    "permissions": ["read", "write", "admin"]
  }'

# Response:
{
  "apiKey": "anythingllm-abc123def456ghi789",
  "name": "My Application",
  "permissions": ["read", "write", "admin"],
  "createdAt": "2024-01-01T00:00:00Z"
}

# Use API key in requests
curl -H "Authorization: Bearer anythingllm-abc123def456ghi789" \
     http://localhost:3001/api/v1/workspaces
```

### API Structure

```yaml
# RESTful API endpoints:

# Authentication
POST   /api/v1/auth/login
POST   /api/v1/auth/api-key
DELETE /api/v1/auth/api-key/{id}

# Workspaces
GET    /api/v1/workspaces
POST   /api/v1/workspaces
GET    /api/v1/workspace/{id}
PUT    /api/v1/workspace/{id}
DELETE /api/v1/workspace/{id}

# Documents
GET    /api/v1/workspace/{id}/documents
POST   /api/v1/workspace/{id}/document/upload
DELETE /api/v1/document/{id}

# Chat
POST   /api/v1/workspace/{id}/chat
GET    /api/v1/workspace/{id}/chats
DELETE /api/v1/workspace/{id}/chat/{id}

# System
GET    /api/v1/system/health
GET    /api/v1/system/info
GET    /api/v1/analytics/*
```

## Workspace Management API

### Creating Workspaces

```bash
# Create workspace programmatically
curl -X POST http://localhost:3001/api/v1/workspace \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Documentation",
    "description": "Technical documentation workspace",
    "settings": {
      "chat_mode": "chat",
      "model": "gpt-4o",
      "temperature": 0.7
    }
  }'

# Response:
{
  "workspace": {
    "id": "ws-123",
    "name": "API Documentation",
    "slug": "api-documentation",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

### Bulk Workspace Operations

```bash
# List all workspaces
curl http://localhost:3001/api/v1/workspaces \
  -H "Authorization: Bearer YOUR_API_KEY"

# Update multiple workspaces
curl -X PUT http://localhost:3001/api/v1/workspaces/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {
        "id": "ws-123",
        "settings": {"model": "claude-3-5-sonnet-20241022"}
      },
      {
        "id": "ws-456",
        "settings": {"temperature": 0.3}
      }
    ]
  }'
```

## Document Management API

### Uploading Documents

```bash
# Upload single file
curl -X POST http://localhost:3001/api/v1/document/upload \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@user-guide.pdf" \
  -F "workspaceId=ws-123"

# Upload from URL
curl -X POST http://localhost:3001/api/v1/document/upload/url \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com/api-ref.pdf",
    "workspaceId": "ws-123",
    "title": "API Reference"
  }'

# Upload with metadata
curl -X POST http://localhost:3001/api/v1/document/upload \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf" \
  -F "workspaceId=ws-123" \
  -F 'metadata={"author": "John Doe", "version": "1.0", "category": "tutorial"}'
```

### Batch Document Operations

```bash
# Upload multiple files
curl -X POST http://localhost:3001/api/v1/document/upload/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "files=@guide1.pdf" \
  -F "files=@guide2.docx" \
  -F "files=@guide3.md" \
  -F "workspaceId=ws-123"

# Get document status
curl http://localhost:3001/api/v1/workspace/ws-123/documents \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "documents": [
    {
      "id": "doc-123",
      "name": "user-guide.pdf",
      "type": "pdf",
      "size": 2457600,
      "status": "processed",
      "chunks": 45,
      "tokens": 12500,
      "uploadedAt": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### Document Search and Filtering

```bash
# Search documents
curl "http://localhost:3001/api/v1/workspace/ws-123/documents/search?q=user+authentication" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Filter by type
curl "http://localhost:3001/api/v1/workspace/ws-123/documents?type=pdf" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Filter by date
curl "http://localhost:3001/api/v1/workspace/ws-123/documents?uploadedAfter=2024-01-01" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Chat API

### Basic Chat

```bash
# Send chat message
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I implement user authentication?",
    "sessionId": "chat-001"
  }'

# Response:
{
  "id": "msg-123",
  "textResponse": "To implement user authentication in your application...",
  "sources": [
    {
      "title": "Authentication Guide",
      "chunk": "...JWT tokens provide stateless authentication...",
      "score": 0.89
    }
  ],
  "sessionId": "chat-001"
}
```

### Streaming Chat

```bash
# Streaming responses for real-time UX
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/chat/stream \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain the OAuth 2.0 flow",
    "sessionId": "chat-002"
  }'

# Response streams as SSE (Server-Sent Events)
# data: {"chunk": "OAuth 2.0", "done": false}
# data: {"chunk": " is an authorization framework", "done": false}
# data: {"chunk": " that enables applications", "done": false}
# data: {"chunk": "...", "done": true}
```

### Chat History and Sessions

```bash
# Get chat history
curl http://localhost:3001/api/v1/workspace/ws-123/chats \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get specific session
curl http://localhost:3001/api/v1/workspace/ws-123/chat/chat-001 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Delete chat session
curl -X DELETE http://localhost:3001/api/v1/workspace/ws-123/chat/chat-001 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Advanced API Features

### Custom Embeddings

```bash
# Upload custom embeddings
curl -X POST http://localhost:3001/api/v1/document/embeddings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "doc-123",
    "embeddings": [
      [0.1, 0.2, 0.3, ...],
      [0.4, 0.5, 0.6, ...]
    ],
    "metadata": {
      "model": "custom-embeddings",
      "dimensions": 768
    }
  }'
```

### Webhook Integration

```bash
# Register webhook for events
curl -X POST http://localhost:3001/api/v1/webhooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://myapp.com/webhook",
    "events": ["document.processed", "chat.created"],
    "secret": "webhook-secret"
  }'

# AnythingLLM will POST to your webhook:
{
  "event": "document.processed",
  "data": {
    "documentId": "doc-123",
    "workspaceId": "ws-456",
    "status": "completed",
    "chunks": 42
  }
}
```

### Rate Limiting

```bash
# Check rate limit status
curl -I http://localhost:3001/api/v1/workspace/ws-123/chat \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response headers:
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 95
# X-RateLimit-Reset: 1640995200
```

## SDK and Client Libraries

### Python SDK

```python
# Install SDK
pip install anythingllm

# Basic usage
from anythingllm import AnythingLLM

client = AnythingLLM(
    api_key="your-api-key",
    base_url="http://localhost:3001"
)

# Create workspace
workspace = client.workspaces.create(
    name="API Docs",
    description="Technical documentation"
)

# Upload document
with open("api-guide.pdf", "rb") as f:
    document = client.documents.upload(
        workspace_id=workspace.id,
        file=f,
        filename="api-guide.pdf"
    )

# Chat with documents
response = client.chat.create(
    workspace_id=workspace.id,
    message="How do I authenticate API requests?",
    session_id="session-001"
)

print(response.text_response)
```

### JavaScript SDK

```javascript
// Install SDK
npm install anythingllm

// Basic usage
const { AnythingLLM } = require('anythingllm');

const client = new AnythingLLM({
  apiKey: 'your-api-key',
  baseURL: 'http://localhost:3001'
});

// Async/await usage
async function main() {
  // Create workspace
  const workspace = await client.workspaces.create({
    name: 'Product Docs',
    description: 'Product documentation workspace'
  });

  // Upload document
  const document = await client.documents.upload(workspace.id, {
    file: fs.createReadStream('user-guide.pdf'),
    filename: 'user-guide.pdf'
  });

  // Chat
  const response = await client.chat.create(workspace.id, {
    message: 'What are the main product features?',
    sessionId: 'chat-001'
  });

  console.log(response.textResponse);
}

main();
```

### Go SDK

```go
// Install SDK
go get github.com/example/anythingllm-go

// Basic usage
package main

import (
    "context"
    "fmt"
    "os"

    anythingllm "github.com/example/anythingllm-go"
)

func main() {
    client := anythingllm.NewClient(
        anythingllm.WithAPIKey("your-api-key"),
        anythingllm.WithBaseURL("http://localhost:3001"),
    )

    ctx := context.Background()

    // Create workspace
    workspace, err := client.Workspaces.Create(ctx, &anythingllm.WorkspaceRequest{
        Name:        "Engineering Docs",
        Description: "Internal engineering documentation",
    })
    if err != nil {
        panic(err)
    }

    // Upload document
    file, err := os.Open("architecture.pdf")
    if err != nil {
        panic(err)
    }
    defer file.Close()

    document, err := client.Documents.Upload(ctx, workspace.ID, file, "architecture.pdf")
    if err != nil {
        panic(err)
    }

    // Chat
    response, err := client.Chat.Create(ctx, workspace.ID, &anythingllm.ChatRequest{
        Message:   "Explain the system architecture",
        SessionID: "session-001",
    })
    if err != nil {
        panic(err)
    }

    fmt.Println(response.TextResponse)
}
```

## Integration Patterns

### Chatbot Integration

```python
# Integrate with existing chatbot platforms
from anythingllm import AnythingLLM
import slack_sdk

class SlackBot:
    def __init__(self):
        self.anythingllm = AnythingLLM(api_key="your-key")
        self.slack = slack_sdk.WebClient(token="slack-token")
        self.workspace_id = "ws-123"  # Your workspace

    def handle_message(self, event):
        user_message = event['text']

        # Get response from AnythingLLM
        response = self.anythingllm.chat.create(
            workspace_id=self.workspace_id,
            message=user_message,
            session_id=f"slack-{event['user']}"
        )

        # Send back to Slack
        self.slack.chat_postMessage(
            channel=event['channel'],
            text=response.text_response
        )
```

### API Gateway Integration

```python
# Use as backend for API gateway
from flask import Flask, request, jsonify
from anythingllm import AnythingLLM

app = Flask(__name__)
anythingllm = AnythingLLM(api_key="your-key")

@app.route('/api/v1/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    workspace_id = data.get('workspace_id', 'default')
    question = data.get('question')

    # Rate limiting check
    if not check_rate_limit(request.remote_addr):
        return jsonify({'error': 'Rate limit exceeded'}), 429

    # Get answer from documents
    response = anythingllm.chat.create(
        workspace_id=workspace_id,
        message=question
    )

    return jsonify({
        'answer': response.text_response,
        'sources': response.sources,
        'confidence': response.confidence
    })

def check_rate_limit(ip):
    # Implement rate limiting logic
    pass
```

### Database Integration

```python
# Store chat history in your database
import sqlite3
from anythingllm import AnythingLLM

class ChatStorage:
    def __init__(self):
        self.conn = sqlite3.connect('chat_history.db')
        self.anythingllm = AnythingLLM(api_key="your-key")
        self._create_tables()

    def _create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                workspace_id TEXT,
                user_id TEXT,
                question TEXT,
                answer TEXT,
                sources TEXT,
                created_at TIMESTAMP
            )
        ''')

    def ask_and_store(self, workspace_id, user_id, question):
        # Get answer from AnythingLLM
        response = self.anythingllm.chat.create(
            workspace_id=workspace_id,
            message=question
        )

        # Store in database
        self.conn.execute('''
            INSERT INTO chats (id, workspace_id, user_id, question, answer, sources, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            response.id,
            workspace_id,
            user_id,
            question,
            response.text_response,
            json.dumps(response.sources)
        ))

        self.conn.commit()
        return response
```

## Monitoring and Analytics

### API Usage Analytics

```bash
# Get API usage statistics
curl http://localhost:3001/api/v1/analytics/api-usage \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "total_requests": 15420,
  "requests_by_endpoint": {
    "/api/v1/workspace/*/chat": 12000,
    "/api/v1/document/upload": 2500,
    "/api/v1/workspaces": 920
  },
  "response_times": {
    "average": 2.3,
    "p95": 5.1,
    "p99": 12.8
  },
  "error_rates": {
    "4xx": 0.02,
    "5xx": 0.005
  }
}
```

### Integration Monitoring

```bash
# Monitor external integrations
curl http://localhost:3001/api/v1/system/integrations/status \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "integrations": [
    {
      "name": "slack_bot",
      "status": "healthy",
      "last_success": "2024-01-01T12:00:00Z",
      "error_count": 0
    },
    {
      "name": "api_gateway",
      "status": "healthy",
      "last_success": "2024-01-01T12:05:00Z",
      "error_count": 2
    }
  ]
}
```

## Security and Compliance

### API Security

```bash
# Use HTTPS in production
# Configure SSL/TLS certificates

# API key rotation
curl -X POST http://localhost:3001/api/v1/auth/api-key/rotate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "currentKey": "anythingllm-abc123...",
    "name": "Rotated API Key"
  }'

# IP whitelisting
# Configure firewall rules to restrict API access
# Only allow trusted IP ranges
```

### Data Privacy

```yaml
# Configure data handling policies
privacy_settings:
  data_retention_days: 365
  anonymize_logs: true
  export_data_on_request: true
  delete_data_on_request: true

# Compliance features:
# - GDPR data export/deletion
# - Audit logging
# - Data encryption at rest
# - Secure API communication
```

### Audit Logging

```bash
# Enable comprehensive audit logging
curl -X PUT http://localhost:3001/api/v1/system/audit \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "log_level": "detailed",
    "retention_days": 2555,
    "events": [
      "api_call",
      "document_upload",
      "chat_created",
      "workspace_modified"
    ]
  }'

# Query audit logs
curl "http://localhost:3001/api/v1/audit/logs?startDate=2024-01-01&eventType=api_call" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Troubleshooting API Issues

### Common API Errors

```bash
# 401 Unauthorized
# - Check API key is valid and not expired
# - Verify correct header format: "Authorization: Bearer <key>"

# 403 Forbidden
# - Check API key has required permissions
# - Verify workspace access permissions

# 429 Too Many Requests
# - Implement exponential backoff
# - Check rate limit headers
# - Consider upgrading plan

# 500 Internal Server Error
# - Check server logs
# - Verify system resources
# - Report to support if persistent
```

### Debugging API Calls

```bash
# Enable API debugging
export API_DEBUG=true

# Log all requests and responses
curl -v http://localhost:3001/api/v1/workspaces \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check system status
curl http://localhost:3001/api/v1/system/health \
  -H "Authorization: Bearer YOUR_API_KEY"

# View detailed error messages
curl http://localhost:3001/api/v1/debug/last-error \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Summary

In this chapter, we've covered:

- **API Fundamentals**: Authentication and basic API structure
- **Workspace Management**: Creating and managing workspaces programmatically
- **Document Operations**: Upload, search, and manage documents via API
- **Chat Integration**: Building chat functionality into applications
- **SDK Libraries**: Python, JavaScript, and Go client libraries
- **Integration Patterns**: Chatbots, API gateways, database storage
- **Monitoring**: Usage analytics and integration health checks
- **Security**: API security, data privacy, and audit logging
- **Troubleshooting**: Common issues and debugging techniques

## Key Takeaways

1. **Comprehensive API**: Full programmatic access to all features
2. **SDK Support**: Client libraries for popular programming languages
3. **Integration Flexibility**: Build AnythingLLM into any application
4. **Security First**: Proper authentication and authorization
5. **Monitoring**: Track usage and performance
6. **Scalability**: Handle high-volume API usage
7. **Compliance**: Audit logging and data privacy features

## Next Steps

Now that you can integrate AnythingLLM programmatically, let's explore **production deployment** with Docker, security hardening, and scaling.

---

**Ready for Chapter 8?** [Production Deployment](08-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*