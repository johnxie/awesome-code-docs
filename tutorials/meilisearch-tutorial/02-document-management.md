---
layout: default
title: "Chapter 2: Document Management"
parent: "MeiliSearch Tutorial"
nav_order: 2
---

# Chapter 2: Document Management

Welcome to **Chapter 2: Document Management**. In this part of **MeiliSearch Tutorial: Lightning Fast Search Engine**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In this chapter, we'll explore how to effectively manage documents in Meilisearch - adding, updating, deleting, and batch operations.

## 📄 Adding Documents

### Single Document

```bash
curl -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "id": 4,
    "title": "Pulp Fiction",
    "director": "Quentin Tarantino",
    "year": 1994,
    "genre": ["Crime", "Drama"],
    "rating": 8.9
  }'
```

### Batch Documents

```bash
curl -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    {
      "id": 5,
      "title": "Fight Club",
      "director": "David Fincher",
      "year": 1999,
      "genre": ["Drama"],
      "rating": 8.8
    },
    {
      "id": 6,
      "title": "Forrest Gump",
      "director": "Robert Zemeckis",
      "year": 1994,
      "genre": ["Drama", "Romance"],
      "rating": 8.8
    }
  ]'
```

### From File

```bash
# Create a JSON file
cat > movies_batch.json << EOF
[
  {"id": 7, "title": "The Lord of the Rings", "director": "Peter Jackson", "year": 2001},
  {"id": 8, "title": "Star Wars", "director": "George Lucas", "year": 1977}
]
EOF

# Upload from file
curl -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data @movies_batch.json
```

## 🔄 Updating Documents

### Update Single Document

```bash
curl -X PUT 'http://localhost:7700/indexes/movies/documents/1' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "title": "The Shawshank Redemption",
    "director": "Frank Darabont",
    "year": 1994,
    "genre": ["Drama", "Crime"],
    "rating": 9.3,
    "duration": 142
  }'
```

### Partial Update

```bash
# Only update specific fields
curl -X PATCH 'http://localhost:7700/indexes/movies/documents/1' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "rating": 9.5,
    "awards": ["Academy Award for Best Picture"]
  }'
```

### Batch Update

```bash
curl -X PUT 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    {"id": 2, "rating": 9.4},
    {"id": 3, "rating": 9.2}
  ]'
```

## 🗑️ Deleting Documents

### Delete Single Document

```bash
curl -X DELETE 'http://localhost:7700/indexes/movies/documents/1' \
  -H 'Authorization: Bearer your_master_key'
```

### Delete Multiple Documents

```bash
curl -X POST 'http://localhost:7700/indexes/movies/documents/delete-batch' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[2, 3, 4]'
```

### Delete by Filter

```bash
# Delete all movies from 1994
curl -X POST 'http://localhost:7700/indexes/movies/documents/delete' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "filter": "year = 1994"
  }'
```

### Clear All Documents

```bash
# Delete all documents in index
curl -X DELETE 'http://localhost:7700/indexes/movies/documents' \
  -H 'Authorization: Bearer your_master_key'
```

## 📊 Retrieving Documents

### Get Single Document

```bash
curl 'http://localhost:7700/indexes/movies/documents/1'
```

### Get Multiple Documents

```bash
curl 'http://localhost:7700/indexes/movies/documents?ids=1,2,3'
```

### Get All Documents

```bash
curl 'http://localhost:7700/indexes/movies/documents'
```

### Paginated Retrieval

```bash
# Get first 10 documents
curl 'http://localhost:7700/indexes/movies/documents?limit=10&offset=0'

# Get next page
curl 'http://localhost:7700/indexes/movies/documents?limit=10&offset=10'
```

## 🔍 Document Search and Filtering

### Search with Filters

```bash
# Search for drama movies
curl 'http://localhost:7700/indexes/movies/search?q=drama&filter=genre=Drama'

# Search by year range
curl 'http://localhost:7700/indexes/movies/search?q=&filter=year>=1990 AND year<=2000'
```

### Advanced Filtering

```bash
# Multiple conditions
curl 'http://localhost:7700/indexes/movies/search?q=movie&filter=(genre=Drama OR genre=Crime) AND rating>=8.5'

# Array field filtering
curl 'http://localhost:7700/indexes/movies/search?q=&filter=genre=Drama'
```

## 📈 Batch Operations

### Large Dataset Import

```bash
# For large datasets, use streaming
curl -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  -H 'Content-Encoding: gzip' \
  --data-binary @large_dataset.json.gz
```

### Asynchronous Operations

```bash
# Meilisearch processes updates asynchronously
# Check task status
curl 'http://localhost:7700/tasks/1'
```

## 🛠️ Document Schema Management

### Displayable Attributes

```bash
# Configure which fields to return in search results
curl -X PUT 'http://localhost:7700/indexes/movies/settings/displayed-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["title", "director", "year", "rating"]'
```

### Searchable Attributes

```bash
# Configure which fields are searchable
curl -X PUT 'http://localhost:7700/indexes/movies/settings/searchable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["title", "director", "genre"]'
```

### Filterable Attributes

```bash
# Configure which fields can be used for filtering
curl -X PUT 'http://localhost:7700/indexes/movies/settings/filterable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["year", "genre", "rating"]'
```

## 📊 Monitoring Document Operations

### Task Monitoring

```bash
# Get all tasks
curl 'http://localhost:7700/tasks'

# Get specific task
curl 'http://localhost:7700/tasks/1'

# Get tasks by status
curl 'http://localhost:7700/tasks?statuses=processing,succeeded'
```

### Index Statistics

```bash
# Get index stats
curl 'http://localhost:7700/indexes/movies/stats'
```

## 🎯 Best Practices

### Document Structure

```javascript
// Good document structure
{
  "id": "unique_identifier",
  "title": "Document Title",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "content": "Full text content for search"
}
```

### Batch Size Optimization

```bash
# Optimal batch size: 1000 documents per request
# For large imports, split into chunks
split -l 1000 large_dataset.json batch_

# Process batches sequentially
for file in batch_*; do
  curl -X POST 'http://localhost:7700/indexes/movies/documents' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer your_master_key' \
    --data @$file
done
```

## 🚨 Error Handling

### Common Errors

```json
// Document too large
{
  "message": "Document is too large",
  "errorCode": "document_too_large",
  "errorType": "invalid_request"
}

// Invalid document format
{
  "message": "Invalid document format",
  "errorCode": "invalid_document_format",
  "errorType": "invalid_request"
}
```

## 📝 Chapter Summary

- ✅ Added single and batch documents
- ✅ Updated documents with PUT and PATCH
- ✅ Deleted documents individually and in batches
- ✅ Retrieved documents with pagination
- ✅ Configured searchable, filterable, and displayable attributes
- ✅ Monitored operations with task system
- ✅ Implemented best practices for document management

**Key Takeaways:**
- Use batch operations for better performance
- Configure attributes properly for optimal search
- Monitor tasks for asynchronous operations
- Handle errors gracefully in production

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `curl`, `http`, `localhost` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Document Management` as an operating subsystem inside **MeiliSearch Tutorial: Lightning Fast Search Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `movies`, `indexes`, `documents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Document Management` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `curl`.
2. **Input normalization**: shape incoming data so `http` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `localhost`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/meilisearch/meilisearch)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `curl` and `http` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Meilisearch](01-getting-started.md)
- [Next Chapter: Chapter 3: Search Fundamentals](03-search-fundamentals.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
