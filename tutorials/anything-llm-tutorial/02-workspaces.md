---
layout: default
title: "AnythingLLM Tutorial - Chapter 2: Workspaces"
nav_order: 2
has_children: false
parent: AnythingLLM Tutorial
---

# Chapter 2: Workspaces - Organizing Your Knowledge

Welcome to **Chapter 2: Workspaces - Organizing Your Knowledge**. In this part of **AnythingLLM Tutorial: Self-Hosted RAG and Agents Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Create and manage workspaces to organize documents, conversations, and knowledge domains.

## Overview

Workspaces are the fundamental organizational unit in AnythingLLM. They allow you to create isolated knowledge bases for different projects, teams, or topics, each with their own documents, chat history, and configuration.

## Workspace Concepts

### What is a Workspace?

A workspace represents a self-contained knowledge domain containing:

- **Documents**: Your source materials
- **Chat History**: Conversation threads
- **Configuration**: Custom settings
- **Embeddings**: Vector representations
- **Access Control**: User permissions

### Use Cases for Workspaces

```yaml
# Project-based organization
Workspaces:
  - "Product Documentation"    # User guides, API docs
  - "Engineering Handbook"     # Internal processes, standards
  - "Research Papers"         # Academic articles, studies
  - "Customer Support"        # FAQ, troubleshooting guides
  - "Legal Documents"         # Contracts, policies, compliance

# Team-based organization
Workspaces:
  - "Frontend Team"           # React docs, UI guidelines
  - "Backend Team"           # API specs, database schemas
  - "DevOps Team"            # Infrastructure docs, runbooks
  - "Product Team"           # Requirements, user research

# Domain-based organization
Workspaces:
  - "Machine Learning"        # ML papers, tutorials
  - "Security"               # Security policies, threat models
  - "Compliance"             # Regulatory documents, audits
```

## Creating Workspaces

### Basic Workspace Creation

```bash
# Via Web Interface
1. Click "New Workspace" in the sidebar
2. Enter workspace name
3. Add description (optional)
4. Choose privacy settings
5. Create workspace
```

### Advanced Workspace Configuration

```json
{
  "name": "Advanced Workspace",
  "description": "Workspace with custom configuration",
  "settings": {
    "chat_mode": "chat",
    "embedding_model": "text-embedding-3-small",
    "similarity_threshold": 0.25,
    "max_tokens": 2048,
    "temperature": 0.7,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  },
  "permissions": {
    "public": false,
    "users": ["user1@example.com", "user2@example.com"],
    "groups": ["engineering", "product"]
  }
}
```

### Workspace Templates

```bash
# Create workspace from template
curl -X POST http://localhost:3001/api/v1/workspace \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Documentation",
    "template": "technical_docs",
    "documents": [
      {"url": "https://api.example.com/docs"},
      {"file": "api-reference.pdf"}
    ]
  }'
```

## Workspace Management

### Listing Workspaces

```bash
# Via API
curl http://localhost:3001/api/v1/workspaces \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response
{
  "workspaces": [
    {
      "id": "ws-123",
      "name": "Product Documentation",
      "description": "User guides and API docs",
      "createdAt": "2024-01-01T00:00:00Z",
      "lastUpdated": "2024-01-02T00:00:00Z",
      "documentCount": 15,
      "messageCount": 234
    }
  ]
}
```

### Updating Workspace Settings

```bash
# Update workspace configuration
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Documentation",
    "description": "Latest user guides and API documentation",
    "settings": {
      "chat_mode": "query",
      "temperature": 0.3
    }
  }'
```

### Workspace Deletion

```bash
# Delete workspace (irreversible!)
curl -X DELETE http://localhost:3001/api/v1/workspace/ws-123 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Or via web interface with confirmation
```

## Document Organization

### Adding Documents to Workspaces

```bash
# Upload single file
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/document \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@user-guide.pdf"

# Upload multiple files
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/documents \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "files=@guide1.pdf" \
  -F "files=@guide2.pdf"

# Add from URL
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/link \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com/api-reference",
    "title": "API Reference"
  }'
```

### Document Management

```bash
# List documents in workspace
curl http://localhost:3001/api/v1/workspace/ws-123/documents \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get document details
curl http://localhost:3001/api/v1/workspace/ws-123/document/doc-456 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Delete document
curl -X DELETE http://localhost:3001/api/v1/workspace/ws-123/document/doc-456 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Document Folders and Organization

```bash
# Create folder structure
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/folder \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Documentation",
    "parentId": null
  }'

# Upload to specific folder
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/document \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@api-guide.pdf" \
  -F "folderId=folder-123"
```

## Chat Management

### Chat Sessions

```bash
# Start new chat session
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the main features?",
    "sessionId": "chat-001"
  }'

# Continue existing chat
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you elaborate on the API authentication?",
    "sessionId": "chat-001"
  }'
```

### Chat History

```bash
# Get chat history
curl http://localhost:3001/api/v1/workspace/ws-123/chats \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get specific chat thread
curl http://localhost:3001/api/v1/workspace/ws-123/chat/chat-001 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Delete chat history
curl -X DELETE http://localhost:3001/api/v1/workspace/ws-123/chat/chat-001 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Chat Settings

```bash
# Configure chat behavior per workspace
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/settings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chat": {
      "mode": "chat",  // "chat" or "query"
      "model": "gpt-4o",
      "temperature": 0.7,
      "maxTokens": 2048,
      "systemPrompt": "You are a helpful assistant that answers questions about our product documentation."
    }
  }'
```

## Access Control

### User Permissions

```bash
# Add user to workspace
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "role": "editor"  // "viewer", "editor", "admin"
  }'

# Update user permissions
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/users/user-123 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'

# Remove user from workspace
curl -X DELETE http://localhost:3001/api/v1/workspace/ws-123/users/user-123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Public Workspaces

```bash
# Make workspace public (read-only)
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/visibility \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public": true,
    "publicReadOnly": true
  }'

# Access public workspace without authentication
curl http://localhost:3001/api/v1/public/workspace/ws-123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is this workspace about?"}'
```

## Workspace Analytics

### Usage Statistics

```bash
# Get workspace analytics
curl http://localhost:3001/api/v1/workspace/ws-123/analytics \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response
{
  "documentCount": 25,
  "totalTokens": 150000,
  "chatCount": 150,
  "messageCount": 450,
  "topQueries": [
    {"query": "how to authenticate", "count": 12},
    {"query": "api limits", "count": 8},
    {"query": "troubleshooting", "count": 6}
  ],
  "usageByDay": [
    {"date": "2024-01-01", "queries": 25, "documents": 2},
    {"date": "2024-01-02", "queries": 30, "documents": 0}
  ]
}
```

### Performance Metrics

```bash
# Get performance data
curl http://localhost:3001/api/v1/workspace/ws-123/metrics \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response
{
  "averageResponseTime": 2.3,
  "querySuccessRate": 0.98,
  "documentProcessingTime": 45.2,
  "vectorSearchTime": 0.15,
  "llmResponseTime": 2.1
}
```

## Workspace Templates

### Creating Templates

```bash
# Save workspace as template
curl -X POST http://localhost:3001/api/v1/templates \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Documentation Template",
    "description": "Standard template for API documentation workspaces",
    "workspaceId": "ws-123"
  }'

# List available templates
curl http://localhost:3001/api/v1/templates \
  -H "Authorization: Bearer YOUR_API_KEY"

# Create workspace from template
curl -X POST http://localhost:3001/api/v1/workspace/from-template \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "template-456",
    "name": "My API Docs",
    "description": "Project-specific API documentation"
  }'
```

### Standard Templates

```yaml
# Predefined templates
templates:
  - name: "Software Documentation"
    description: "For software projects and technical documentation"
    folders: ["Guides", "API Reference", "Tutorials", "Troubleshooting"]
    settings:
      chat_mode: "query"
      temperature: 0.3

  - name: "Research Papers"
    description: "For academic and research document collections"
    folders: ["Papers", "Notes", "References", "Summaries"]
    settings:
      chat_mode: "chat"
      temperature: 0.7
      max_tokens: 4096

  - name: "Customer Support"
    description: "For support documentation and FAQs"
    folders: ["FAQ", "Troubleshooting", "How-to Guides", "Contact Info"]
    settings:
      chat_mode: "chat"
      temperature: 0.8
```

## Workspace Migration

### Exporting Workspaces

```bash
# Export workspace configuration
curl -X GET http://localhost:3001/api/v1/workspace/ws-123/export \
  -H "Authorization: Bearer YOUR_API_KEY" \
  --output workspace-config.json

# Export with documents (large files)
curl -X GET "http://localhost:3001/api/v1/workspace/ws-123/export?includeDocuments=true" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  --output workspace-backup.tar.gz
```

### Importing Workspaces

```bash
# Import workspace configuration
curl -X POST http://localhost:3001/api/v1/workspace/import \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "config=@workspace-config.json"

# Import complete workspace
curl -X POST http://localhost:3001/api/v1/workspace/import \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "backup=@workspace-backup.tar.gz"
```

## Advanced Workspace Features

### Workspace Hooks

```bash
# Webhooks for workspace events
curl -X POST http://localhost:3001/api/v1/workspace/ws-123/hooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/webhook",
    "events": ["document.added", "chat.created", "workspace.updated"],
    "secret": "webhook-secret"
  }'
```

### Custom Embeddings

```bash
# Use custom embedding models
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/embeddings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "custom-embedding-model",
    "dimensions": 768,
    "apiKey": "custom-api-key"
  }'
```

### Workspace Limits

```bash
# Set resource limits per workspace
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/limits \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "maxDocuments": 1000,
    "maxFileSize": "100MB",
    "maxQueriesPerHour": 1000,
    "maxTokensPerQuery": 4096
  }'
```

## Best Practices

### Organization Strategies

```yaml
# Effective workspace organization:

# 1. Purpose-driven workspaces
# - One workspace per major project/component
# - Separate workspaces for different user types
# - Isolated workspaces for sensitive information

# 2. Size considerations
# - Keep workspaces under 1000 documents
# - Balance breadth vs depth of content
# - Consider performance impact of large workspaces

# 3. Access control
# - Use role-based access (viewer/editor/admin)
# - Regular audit of user permissions
# - Consider workspace visibility requirements
```

### Performance Optimization

```yaml
# Optimize workspace performance:

# 1. Document organization
# - Use folders for logical grouping
# - Remove outdated documents regularly
# - Compress large documents when possible

# 2. Query optimization
# - Use appropriate similarity thresholds
# - Configure chunk sizes for content type
# - Monitor and tune vector search parameters

# 3. Resource management
# - Set appropriate rate limits
# - Monitor usage patterns
# - Scale vector database as needed
```

### Maintenance Tasks

```bash
# Regular maintenance:

# 1. Content updates
# - Review and update documents quarterly
# - Archive old chat histories
# - Update embeddings after major content changes

# 2. Performance monitoring
# - Monitor query response times
# - Track document processing times
# - Review usage analytics regularly

# 3. Security audits
# - Audit user access regularly
# - Review workspace permissions
# - Update security settings as needed
```

## Summary

In this chapter, we've covered:

- **Workspace Creation**: Basic and advanced workspace setup
- **Document Management**: Adding, organizing, and managing documents
- **Chat Management**: Sessions, history, and configuration
- **Access Control**: User permissions and public workspaces
- **Analytics**: Usage statistics and performance metrics
- **Templates**: Creating and using workspace templates
- **Migration**: Exporting and importing workspaces
- **Advanced Features**: Hooks, custom embeddings, and limits

## Key Takeaways

1. **Organization**: Use workspaces to separate knowledge domains
2. **Access Control**: Implement appropriate permission levels
3. **Performance**: Monitor and optimize workspace performance
4. **Maintenance**: Regular content updates and security audits
5. **Templates**: Use templates for consistent workspace setup
6. **Analytics**: Track usage and performance metrics

## Next Steps

Now that you understand workspace organization, let's explore **document upload and processing** in detail.

---

**Ready for Chapter 3?** [Document Upload](03-documents.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `workspace`, `curl`, `http` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Workspaces - Organizing Your Knowledge` as an operating subsystem inside **AnythingLLM Tutorial: Self-Hosted RAG and Agents Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `localhost`, `Authorization`, `Bearer` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Workspaces - Organizing Your Knowledge` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `workspace`.
2. **Input normalization**: shape incoming data so `curl` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `http`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [AnythingLLM Repository](https://github.com/Mintplex-Labs/anything-llm)
  Why it matters: authoritative reference on `AnythingLLM Repository` (github.com).
- [AnythingLLM Releases](https://github.com/Mintplex-Labs/anything-llm/releases)
  Why it matters: authoritative reference on `AnythingLLM Releases` (github.com).
- [AnythingLLM Docs](https://docs.anythingllm.com/)
  Why it matters: authoritative reference on `AnythingLLM Docs` (docs.anythingllm.com).
- [AnythingLLM Website](https://anythingllm.com/)
  Why it matters: authoritative reference on `AnythingLLM Website` (anythingllm.com).

Suggested trace strategy:
- search upstream code for `workspace` and `curl` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with AnythingLLM](01-getting-started.md)
- [Next Chapter: Chapter 3: Document Upload and Processing](03-documents.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
