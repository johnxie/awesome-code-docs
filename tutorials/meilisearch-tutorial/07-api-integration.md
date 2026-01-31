---
layout: default
title: "Chapter 7: API Integration"
parent: "MeiliSearch Tutorial"
nav_order: 7
---

# Chapter 7: API Integration

This chapter covers integrating Meilisearch with various applications using its REST API and available SDKs.

## 🌐 REST API Overview

### Base URL and Authentication

```bash
# Base URL
BASE_URL="http://localhost:7700"

# Authentication header
AUTH_HEADER="Authorization: Bearer your_master_key"

# Health check
curl "$BASE_URL/health"
```

### API Endpoints Structure

```javascript
const endpoints = {
  // Indexes
  indexes: '/indexes',
  index: '/indexes/{index_uid}',

  // Documents
  documents: '/indexes/{index_uid}/documents',
  document: '/indexes/{index_uid}/documents/{document_id}',

  // Search
  search: '/indexes/{index_uid}/search',

  // Settings
  settings: '/indexes/{index_uid}/settings',
  rankingRules: '/indexes/{index_uid}/settings/ranking-rules',

  // Tasks
  tasks: '/tasks',
  task: '/tasks/{task_uid}'
};
```

## 📱 JavaScript SDK

### Installation

```bash
npm install meilisearch
```

### Basic Usage

```javascript
import { MeiliSearch } from 'meilisearch'

const client = new MeiliSearch({
  host: 'http://localhost:7700',
  apiKey: 'your_master_key'
})

// Create index
await client.createIndex('movies')

// Add documents
await client.index('movies').addDocuments([
  { id: 1, title: 'Inception', year: 2010 },
  { id: 2, title: 'Interstellar', year: 2014 }
])

// Search
const results = await client.index('movies').search('inception')
console.log(results.hits)
```

### Advanced Search

```javascript
// Advanced search with filters
const searchParams = {
  q: 'movie',
  filter: 'year >= 2010 AND genre = "Sci-Fi"',
  sort: ['year:desc'],
  limit: 20,
  attributesToRetrieve: ['title', 'year', 'rating']
}

const results = await client.index('movies').search('', searchParams)
```

## 🐍 Python SDK

### Installation

```bash
pip install meilisearch
```

### Usage

```python
from meilisearch import Client

client = Client('http://localhost:7700', 'your_master_key')

# Create index
index = client.create_index('products')

# Add documents
documents = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 29.99}
]
index.add_documents(documents)

# Search
results = index.search('laptop')
print(results['hits'])
```

### Async Usage

```python
import asyncio
from meilisearch import Client

async def search_products():
    client = Client('http://localhost:7700', 'your_master_key')
    index = client.get_index('products')

    results = await index.search('laptop')
    return results

# Run async search
results = asyncio.run(search_products())
```

## 📘 Other SDKs

### Go SDK

```go
package main

import (
    "fmt"
    "github.com/meilisearch/meilisearch-go"
)

func main() {
    client := meilisearch.NewClient(meilisearch.ClientConfig{
        Host:   "http://localhost:7700",
        APIKey: "your_master_key",
    })

    // Create index
    _, err := client.CreateIndex(&meilisearch.IndexConfig{
        Uid: "books",
    })

    // Add documents
    books := []map[string]interface{}{
        {"id": 1, "title": "1984", "author": "George Orwell"},
    }

    _, err = client.Index("books").AddDocuments(books)

    // Search
    results, err := client.Index("books").Search("1984",
        &meilisearch.SearchRequest{})

    fmt.Println(results.Hits)
}
```

### PHP SDK

```php
<?php

require_once 'vendor/autoload.php';

use MeiliSearch\Client;

$client = new Client('http://localhost:7700', 'your_master_key');

// Create index
$client->createIndex('articles');

// Add documents
$documents = [
    ['id' => 1, 'title' => 'PHP Tutorial', 'content' => 'Learn PHP'],
];
$client->index('articles')->addDocuments($documents);

// Search
$results = $client->index('articles')->search('PHP');
echo json_encode($results['hits']);
```

## 🔧 Custom Integration

### HTTP Client Integration

```javascript
class MeiliSearchClient {
  constructor(baseURL, apiKey) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
    this.headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.headers,
      ...options
    };

    const response = await fetch(url, config);
    return response.json();
  }

  async search(index, query, params = {}) {
    const searchParams = new URLSearchParams({ q: query, ...params });
    return this.request(`/indexes/${index}/search?${searchParams}`);
  }

  async addDocuments(index, documents) {
    return this.request(`/indexes/${index}/documents`, {
      method: 'POST',
      body: JSON.stringify(documents)
    });
  }
}

// Usage
const client = new MeiliSearchClient('http://localhost:7700', 'your_key');
const results = await client.search('movies', 'inception');
```

### React Integration

```jsx
import React, { useState, useEffect } from 'react';
import { MeiliSearch } from 'meilisearch';

const SearchComponent = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [client] = useState(() => new MeiliSearch({
    host: 'http://localhost:7700',
    apiKey: 'your_master_key'
  }));

  const search = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    try {
      const searchResults = await client.index('products').search(searchQuery);
      setResults(searchResults.hits);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(() => search(query), 300);
    return () => clearTimeout(timeoutId);
  }, [query]);

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
      <ul>
        {results.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
};
```

### Vue.js Integration

```vue
<template>
  <div>
    <input v-model="query" @input="debouncedSearch" placeholder="Search..." />
    <div v-for="result in results" :key="result.id">
      {{ result.title }}
    </div>
  </div>
</template>

<script>
import { MeiliSearch } from 'meilisearch';

export default {
  data() {
    return {
      query: '',
      results: [],
      client: null,
      searchTimeout: null
    };
  },
  mounted() {
    this.client = new MeiliSearch({
      host: 'http://localhost:7700',
      apiKey: 'your_master_key'
    });
  },
  methods: {
    debouncedSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.performSearch();
      }, 300);
    },
    async performSearch() {
      if (!this.query.trim()) {
        this.results = [];
        return;
      }

      try {
        const searchResults = await this.client.index('movies').search(this.query);
        this.results = searchResults.hits;
      } catch (error) {
        console.error('Search error:', error);
      }
    }
  }
};
</script>
```

## 🚀 Advanced Integration Patterns

### Service Layer Pattern

```javascript
class SearchService {
  constructor(client) {
    this.client = client;
  }

  async searchWithAnalytics(query, userId, filters = {}) {
    const startTime = Date.now();

    try {
      const results = await this.client.index('products').search(query, filters);

      // Track analytics
      await this.trackSearch(query, results, userId, Date.now() - startTime);

      return results;
    } catch (error) {
      await this.trackError(query, error, userId);
      throw error;
    }
  }

  async trackSearch(query, results, userId, responseTime) {
    // Send to analytics service
    analytics.track('search_performed', {
      query,
      resultCount: results.estimatedTotalHits,
      userId,
      responseTime
    });
  }
}
```

### Caching Layer

```javascript
class CachedSearchService {
  constructor(client, cache) {
    this.client = client;
    this.cache = cache;
    this.ttl = 300000; // 5 minutes
  }

  async search(query, filters = {}) {
    const cacheKey = this.generateCacheKey(query, filters);
    const cached = await this.cache.get(cacheKey);

    if (cached) {
      return cached;
    }

    const results = await this.client.index('products').search(query, filters);
    await this.cache.set(cacheKey, results, this.ttl);

    return results;
  }

  generateCacheKey(query, filters) {
    return `${query}:${JSON.stringify(filters)}`;
  }
}
```

## 🔒 Security Best Practices

### API Key Management

```javascript
// Use different keys for different operations
const keys = {
  search: 'search_only_key',     // Read-only
  admin: 'full_access_key',      // Full access
  tenant1: 'tenant1_key'         // Tenant-specific
};

// Rotate keys regularly
class KeyManager {
  async rotateKeys() {
    const newKey = await this.generateNewKey();
    await this.updateApplicationConfig(newKey);
    await this.revokeOldKey();
  }
}
```

### Request Validation

```javascript
// Validate search requests
const validateSearchRequest = (req) => {
  const { q, limit, offset } = req.query;

  if (!q || q.length > 100) {
    throw new Error('Invalid query');
  }

  if (limit && (limit < 1 || limit > 100)) {
    throw new Error('Invalid limit');
  }

  return { q, limit: limit || 20, offset: offset || 0 };
};
```

## 📊 Monitoring Integration

### Health Checks

```javascript
// Implement health checks
const healthCheck = async (client) => {
  try {
    const health = await client.health();
    return health.status === 'available';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};
```

### Performance Monitoring

```javascript
// Monitor search performance
class SearchMonitor {
  constructor() {
    this.metrics = [];
  }

  async monitorSearch(searchFn, ...args) {
    const startTime = Date.now();
    const result = await searchFn(...args);
    const duration = Date.now() - startTime;

    this.metrics.push({
      duration,
      resultCount: result.estimatedTotalHits,
      timestamp: new Date()
    });

    return result;
  }

  getMetrics() {
    return {
      averageResponseTime: this.calculateAverage(this.metrics.map(m => m.duration)),
      totalSearches: this.metrics.length,
      recentPerformance: this.metrics.slice(-10)
    };
  }
}
```

## 🚨 Error Handling

### Retry Logic

```javascript
// Implement retry for failed requests
const searchWithRetry = async (client, query, maxRetries = 3) => {
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await client.index('products').search(query);
    } catch (error) {
      lastError = error;

      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
      }
    }
  }

  throw lastError;
};
```

### Circuit Breaker

```javascript
// Implement circuit breaker pattern
class CircuitBreaker {
  constructor(failureThreshold = 5, timeout = 60000) {
    this.failureThreshold = failureThreshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Integrated Meilisearch with REST API
- ✅ Used official SDKs for JavaScript, Python, Go, PHP
- ✅ Built custom integrations for React and Vue.js
- ✅ Implemented advanced patterns (service layer, caching)
- ✅ Added security best practices and monitoring
- ✅ Handled errors with retry logic and circuit breaker

**Key Takeaways:**
- REST API is simple and powerful for integration
- Official SDKs provide excellent developer experience
- Implement proper error handling and retries
- Use caching for better performance
- Monitor search performance and health
- Secure API keys and validate requests
