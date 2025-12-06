---
layout: default
title: "n8n AI Tutorial - Chapter 5: RAG Workflows"
nav_order: 5
has_children: false
parent: n8n AI Tutorial
---

# Chapter 5: Retrieval-Augmented Generation (RAG)

> Build knowledge-based AI systems that retrieve relevant information and generate accurate responses.

## RAG Fundamentals

RAG combines retrieval of relevant documents with generative AI to provide accurate, context-aware responses.

## Document Ingestion Pipeline

### File Upload and Processing

```json
{
  "nodes": [
    {
      "parameters": {
        "operation": "upload",
        "binaryData": true,
        "options": {}
      },
      "name": "File Upload",
      "type": "n8n-nodes-base.filesReadWrite",
      "typeVersion": 1
    },
    {
      "parameters": {
        "operation": "pdfToText",
        "binaryData": true,
        "dataPropertyName": "data"
      },
      "name": "PDF Extractor",
      "type": "n8n-nodes-base.extractFromFile"
    },
    {
      "parameters": {
        "dataPropertyName": "data",
        "extractionValues": {
          "values": [
            {
              "key": "title",
              "cssSelector": "title",
              "returnValue": "text"
            },
            {
              "key": "content",
              "cssSelector": "body",
              "returnValue": "text"
            }
          ]
        }
      },
      "name": "HTML Extractor",
      "type": "n8n-nodes-base.html"
    }
  ]
}
```

### Document Chunking

```javascript
// Smart document chunking
const text = $input.item.json.document_text;
const chunkSize = 1000;
const overlap = 200;

const chunks = [];
for (let i = 0; i < text.length; i += chunkSize - overlap) {
  const chunk = text.slice(i, i + chunkSize);
  chunks.push({
    text: chunk,
    chunk_id: i,
    start_pos: i,
    end_pos: Math.min(i + chunkSize, text.length)
  });
}

return chunks.map(chunk => ({ json: chunk }));
```

## Vector Embeddings

### Embedding Generation

```json
{
  "parameters": {
    "model": "text-embedding-ada-002",
    "input": "={{ $json.chunks.map(c => c.text) }}"
  },
  "name": "Generate Embeddings",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Local Embeddings with Ollama

```json
{
  "parameters": {
    "baseUrl": "http://localhost:11434",
    "model": "nomic-embed-text",
    "prompt": "{{ $json.chunk_text }}"
  },
  "name": "Local Embeddings",
  "type": "@n8n/n8n-nodes-langchain.ollama"
}
```

## Vector Database Storage

### Pinecone Integration

```json
{
  "parameters": {
    "operation": "upsert",
    "pineconeIndex": "knowledge-base",
    "items": "={{ $json.embeddings.map((emb, i) => ({ id: $json.chunk_ids[i], values: emb, metadata: { text: $json.chunks[i].text, source: $json.source } })) }}"
  },
  "name": "Store in Pinecone",
  "type": "@n8n/n8n-nodes-langchain.pinecone",
  "credentials": {
    "pineconeApi": "pinecone-api"
  }
}
```

### Qdrant Integration

```json
{
  "parameters": {
    "operation": "upsert",
    "qdrantCollection": "documents",
    "items": "={{ $json.embeddings.map((emb, i) => ({ id: $json.chunk_ids[i], vector: emb, payload: { text: $json.chunks[i].text, metadata: $json.metadata } })) }}"
  },
  "name": "Store in Qdrant",
  "type": "@n8n/n8n-nodes-langchain.qdrant",
  "credentials": {
    "qdrantApi": "qdrant-api"
  }
}
```

## Query Processing

### Similarity Search

```json
{
  "parameters": {
    "operation": "getMany",
    "pineconeIndex": "knowledge-base",
    "query": "={{ $json.query_embedding }}",
    "numberOfResults": 5,
    "includeValues": false,
    "includeMetadata": true
  },
  "name": "Retrieve Context",
  "type": "@n8n/n8n-nodes-langchain.pinecone"
}
```

### Context Preparation

```javascript
// Combine retrieved documents
const retrieved = $input.all();
const context = retrieved.map(item => item.json.metadata.text).join('\n\n');

return [{
  json: {
    context: context,
    sources: retrieved.map(item => ({
      text: item.json.metadata.text,
      score: item.json.score,
      source: item.json.metadata.source
    })),
    total_chunks: retrieved.length
  }
}];
```

## RAG Response Generation

### Context-Augmented Prompting

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant. Use the provided context to answer questions accurately. If the context doesn't contain the answer, say so."
      },
      {
        "role": "user",
        "content": "Context:\n{{ $json.context }}\n\nQuestion: {{ $json.question }}\n\nAnswer based on the context:"
      }
    ],
    "maxTokens": 500
  },
  "name": "Generate RAG Response",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Multi-Hop Reasoning

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "user",
            "content": "Based on this context, what specific questions should I ask to get more information?\n\nContext: {{ $json.context }}\n\nQuestion: {{ $json.original_question }}"
          }
        ]
      },
      "name": "Generate Follow-up Questions",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "operation": "getMany",
        "pineconeIndex": "knowledge-base",
        "query": "={{ $json.followup_embedding }}",
        "numberOfResults": 3
      },
      "name": "Retrieve Additional Context",
      "type": "@n8n/n8n-nodes-langchain.pinecone"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "user",
            "content": "Original context: {{ $json.original_context }}\nAdditional context: {{ $json.additional_context }}\n\nProvide a comprehensive answer to: {{ $json.original_question }}"
          }
        ]
      },
      "name": "Final Answer Generation",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Advanced RAG Patterns

### Hybrid Search

```javascript
// Combine semantic and keyword search
const query = $input.item.json.query;
const keywords = query.toLowerCase().split(' ');

// Semantic search results
const semanticResults = $input.item.json.semantic_results;

// Keyword filtering
const hybridResults = semanticResults.filter(result => {
  const text = result.metadata.text.toLowerCase();
  return keywords.some(keyword => text.includes(keyword));
});

// Re-rank by keyword matches
hybridResults.forEach(result => {
  const text = result.metadata.text.toLowerCase();
  result.keyword_matches = keywords.filter(k => text.includes(k)).length;
  result.hybrid_score = result.score * (1 + result.keyword_matches * 0.1);
});

hybridResults.sort((a, b) => b.hybrid_score - a.hybrid_score);

return [{
  json: {
    results: hybridResults.slice(0, 5),
    search_type: "hybrid"
  }
}];
```

### Query Expansion

```json
{
  "parameters": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Generate 3 related search queries for: {{ $json.original_query }}"
      }
    ]
  },
  "name": "Query Expansion",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Re-ranking

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": "Rank these documents by relevance to the query: {{ $json.query }}\n\nDocuments:\n{{ $json.documents.map((d, i) => `${i+1}. ${d.text}`).join('\\n') }}\n\nReturn rankings as JSON array."
      }
    ],
    "responseFormat": "json"
  },
  "name": "Re-rank Results",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Knowledge Base Management

### Incremental Updates

```json
{
  "nodes": [
    {
      "parameters": {
        "resource": "file",
        "operation": "watch",
        "path": "./knowledge-base/",
        "options": {
          "watchFor": "files"
        }
      },
      "name": "File Watcher",
      "type": "n8n-nodes-base.filesReadWrite"
    },
    {
      "parameters": {
        "operation": "pdfToText",
        "binaryData": true
      },
      "name": "Process New Document",
      "type": "n8n-nodes-base.extractFromFile"
    },
    {
      "parameters": {
        "model": "text-embedding-ada-002",
        "input": "={{ $json.chunks }}"
      },
      "name": "Embed New Content",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "operation": "upsert",
        "pineconeIndex": "knowledge-base",
        "items": "={{ $json.new_embeddings.map((emb, i) => ({ id: `doc_${Date.now()}_${i}`, values: emb, metadata: { text: $json.chunks[i], source: $json.filename, timestamp: new Date().toISOString() } })) }}"
      },
      "name": "Update Vector DB",
      "type": "@n8n/n8n-nodes-langchain.pinecone"
    }
  ]
}
```

### Version Control

```json
{
  "parameters": {
    "dataToSave": {
      "version": "={{ Date.now() }}",
      "document_count": "={{ $json.total_documents }}",
      "last_updated": "={{ new Date().toISOString() }}",
      "index_stats": "={{ $json.index_stats }}"
    },
    "keys": {
      "type": "kb_version"
    }
  },
  "name": "Version Control",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow"
}
```

## Performance Optimization

### Caching Strategy

```json
{
  "parameters": {
    "dataToSave": {
      "query": "={{ $json.query }}",
      "response": "={{ $json.response }}",
      "context": "={{ $json.context }}",
      "timestamp": "={{ new Date().toISOString() }}"
    },
    "keys": {
      "query_hash": "={{ $json.query_hash }}"
    },
    "ttl": 3600
  },
  "name": "Response Cache",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow"
}
```

### Batch Processing

```json
{
  "parameters": {
    "batchSize": 10,
    "options": {
      "merge": false
    }
  },
  "name": "Batch Embeddings",
  "type": "n8n-nodes-base.splitInBatches"
}
```

## Monitoring and Analytics

### Usage Tracking

```javascript
// Track RAG performance
const ragMetrics = $workflow.expression.get('rag_metrics') || {
  total_queries: 0,
  avg_retrieval_time: 0,
  avg_generation_time: 0,
  cache_hit_rate: 0
};

ragMetrics.total_queries += 1;

if ($input.item.json.cached) {
  ragMetrics.cache_hits = (ragMetrics.cache_hits || 0) + 1;
}

ragMetrics.cache_hit_rate = (ragMetrics.cache_hits || 0) / ragMetrics.total_queries;

$workflow.expression.set('rag_metrics', ragMetrics);

return [{
  json: {
    metrics: ragMetrics,
    query_id: `query_${Date.now()}`
  }
}];
```

### Quality Assessment

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": "Evaluate this RAG response for:\n1. Accuracy\n2. Completeness\n3. Relevance\n4. Helpfulness\n\nResponse: {{ $json.rag_response }}\nContext: {{ $json.context_used }}\nQuery: {{ $json.original_query }}\n\nProvide scores 1-10 and brief explanation."
      }
    ],
    "responseFormat": "json"
  },
  "name": "Quality Assessment",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Best Practices

1. **Chunking Strategy**: Balance chunk size with semantic coherence
2. **Embedding Selection**: Choose embeddings that match your domain
3. **Index Optimization**: Regularly maintain and optimize vector indexes
4. **Caching**: Implement intelligent caching for frequent queries
5. **Monitoring**: Track retrieval quality and response accuracy
6. **Updates**: Implement incremental updates for changing knowledge
7. **Security**: Validate and sanitize retrieved content
8. **Scalability**: Design for growing knowledge bases

RAG transforms static documents into interactive knowledge systems. The next chapter explores AI-powered decision making and routing logic. 