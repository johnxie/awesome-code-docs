---
layout: default
title: "Chapter 5: Filtering & Facets"
parent: "MeiliSearch Tutorial"
nav_order: 5
---

# Chapter 5: Filtering & Facets

Welcome to **Chapter 5: Filtering & Facets**. In this part of **MeiliSearch Tutorial: Lightning Fast Search Engine**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers advanced filtering capabilities and faceted search in Meilisearch, enabling powerful query refinement and analytics.

## 🔍 Basic Filtering

### Filterable Attributes Setup

```bash
# Configure which attributes can be filtered
curl -X PUT 'http://localhost:7700/indexes/movies/settings/filterable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["genre", "year", "rating", "director"]'
```

### Simple Filters

```bash
# Filter by single value
curl 'http://localhost:7700/indexes/movies/search?q=movie&filter=genre=Drama'

# Filter by multiple values
curl 'http://localhost:7700/indexes/movies/search?q=movie&filter=genre="Action" OR genre="Adventure"'
```

### Numeric Filters

```bash
# Numeric comparisons
curl 'http://localhost:7700/indexes/movies/search?q=&filter=year>=2000'

# Range filters
curl 'http://localhost:7700/indexes/movies/search?q=&filter=rating>=8.0 AND rating<=9.0'
```

## 🎯 Advanced Filtering

### Complex Boolean Logic

```bash
# AND conditions
curl 'http://localhost:7700/indexes/movies/search?q=&filter=genre=Drama AND year>=1990'

# OR conditions
curl 'http://localhost:7700/indexes/movies/search?q=&filter=director="Christopher Nolan" OR director="Steven Spielberg"'

# Mixed conditions
curl 'http://localhost:7700/indexes/movies/search?q=&filter=(genre=Action OR genre=Adventure) AND rating>=8.5'
```

### Array Field Filters

```bash
# Filter array contains
curl 'http://localhost:7700/indexes/movies/search?q=&filter=genre=Drama'

# Filter array exact match
curl 'http://localhost:7700/indexes/movies/search?q=&filter=genre=["Drama", "Crime"]'
```

### Nested Filtering

```bash
# Filter with parentheses for complex logic
curl 'http://localhost:7700/indexes/movies/search?q=&filter=(genre=Drama OR genre=Crime) AND (year>=1990 AND year<=2020)'
```

## 📊 Faceted Search

### Basic Facets

```bash
# Get facet distribution
curl 'http://localhost:7700/indexes/movies/search?q=movie&facets=["genre","year"]'
```

**Response:**
```json
{
  "hits": [...],
  "facetDistribution": {
    "genre": {
      "Drama": 25,
      "Action": 18,
      "Comedy": 15,
      "Thriller": 12
    },
    "year": {
      "2023": 8,
      "2022": 12,
      "2021": 15,
      "2020": 10
    }
  }
}
```

### Filtered Facets

```bash
# Get facets for filtered results
curl 'http://localhost:7700/indexes/movies/search?q=&filter=year>=2020&facets=["genre"]'
```

### Facet Limits

```bash
# Limit facet values
curl 'http://localhost:7700/indexes/movies/search?q=&facets=["genre:3"]'
```

## 🔧 Facet Configuration

### Facetable Attributes

```bash
# Configure attributes for faceting
curl -X PUT 'http://localhost:7700/indexes/movies/settings/facetable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["genre", "year", "rating", "director"]'
```

### Facet Search

```bash
# Search within facets
curl 'http://localhost:7700/indexes/movies/facets/genre/search?q=dr'
```

**Response:**
```json
{
  "facetHits": [
    {
      "value": "Drama",
      "count": 25
    },
    {
      "value": "Adventure",
      "count": 18
    }
  ]
}
```

## 🎨 Advanced Facet Features

### Range Facets

```bash
# Numeric ranges
curl 'http://localhost:7700/indexes/movies/search?q=&facets=["rating:2.5:10:1"]'
```

### Custom Facet Ordering

```bash
# Sort facets by count or value
curl 'http://localhost:7700/indexes/movies/search?q=&facets=["genre:count"]'
```

## 📱 Real-World Examples

### E-commerce Search

```javascript
// Product search with filters
const searchProducts = async (query, filters) => {
  const params = new URLSearchParams({
    q: query,
    filter: filters.join(' AND '),
    facets: ['category', 'brand', 'price_range']
  });

  const response = await fetch(`/search?${params}`);
  return response.json();
};

// Usage
const results = await searchProducts('laptop', [
  'category=electronics',
  'price>=500 AND price<=2000',
  'brand="Apple" OR brand="Dell"'
]);
```

### Content Management

```javascript
// Article search with facets
const searchArticles = async (query, filters) => {
  const response = await fetch('/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: query,
      filter: filters,
      facets: ['category', 'author', 'publish_date', 'tags']
    })
  });

  return response.json();
};
```

## 🚀 Performance Optimization

### Filter Performance

```bash
# Use indexed attributes for better performance
curl -X PUT 'http://localhost:7700/indexes/movies/settings/filterable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["genre", "year", "rating"]'  # Only frequently filtered attributes
```

### Facet Caching

```javascript
// Cache facet distributions for better performance
class FacetCache {
  constructor() {
    this.cache = new Map();
    this.ttl = 300000; // 5 minutes
  }

  async getFacets(index, attributes) {
    const key = `${index}-${attributes.join(',')}`;
    const cached = this.cache.get(key);

    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.data;
    }

    const response = await fetch(`/indexes/${index}/search?facets=${attributes}`);
    const data = await response.json();

    this.cache.set(key, { data, timestamp: Date.now() });
    return data;
  }
}
```

## 📊 Analytics and Insights

### Filter Usage Tracking

```javascript
// Track filter usage for analytics
const trackFilters = (filters, results) => {
  analytics.track('search_filters_used', {
    filters: filters,
    resultCount: results.estimatedTotalHits,
    facets: Object.keys(results.facetDistribution || {})
  });
};
```

### Popular Filters

```javascript
// Identify most used filters
const getPopularFilters = async () => {
  const response = await fetch('/analytics/filters/popular');
  return response.json();
};
```

## 🎯 Best Practices

### Filter Design

```javascript
// Good filter design
const goodFilters = {
  category: ['electronics', 'clothing', 'books'],
  priceRange: [0, 50, 100, 500, 1000],
  rating: [1, 2, 3, 4, 5]
};

// Avoid over-filtering
const avoidThis = {
  tooManyOptions: Array.from({length: 100}, (_, i) => `option${i}`),
  tooGranular: [1.1, 1.2, 1.3, 1.4, 1.5] // Too many decimal places
};
```

### Facet Display

```javascript
// Smart facet display
const displayFacets = (facets) => {
  return Object.entries(facets)
    .filter(([_, count]) => count > 0) // Hide empty facets
    .sort((a, b) => b[1] - a[1]) // Sort by count
    .slice(0, 10); // Limit display
};
```

## 🚨 Common Issues

### Filter Not Working

```bash
# Check if attribute is filterable
curl 'http://localhost:7700/indexes/movies/settings/filterable-attributes'

# Add attribute to filterable list
curl -X PUT 'http://localhost:7700/indexes/movies/settings/filterable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["genre", "year", "rating", "new_attribute"]'
```

### Facet Performance Issues

```bash
# Limit facetable attributes
curl -X PUT 'http://localhost:7700/indexes/movies/settings/facetable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["genre", "year"]'  # Only essential facets
```

## 🔧 Advanced Techniques

### Dynamic Filters

```javascript
// Generate filters based on user context
const buildDynamicFilters = (userPreferences, searchContext) => {
  const filters = [];

  if (userPreferences.location) {
    filters.push(`location="${userPreferences.location}"`);
  }

  if (searchContext.category) {
    filters.push(`category=${searchContext.category}`);
  }

  return filters.join(' AND ');
};
```

### Filter Suggestions

```javascript
// Suggest related filters
const suggestFilters = async (currentQuery, currentFilters) => {
  const response = await fetch('/search/suggestions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      q: currentQuery,
      currentFilters: currentFilters
    })
  });

  return response.json();
};
```

## 📝 Chapter Summary

- ✅ Configured filterable and facetable attributes
- ✅ Implemented basic and advanced filters
- ✅ Used faceted search for analytics
- ✅ Optimized filter performance
- ✅ Built real-world search interfaces
- ✅ Troubleshot common filtering issues

**Key Takeaways:**
- Filters enable precise result refinement
- Facets provide search analytics and navigation
- Performance depends on indexed attributes
- Balance filter complexity with usability
- Cache facets for better performance

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `indexes`, `curl`, `http` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Filtering & Facets` as an operating subsystem inside **MeiliSearch Tutorial: Lightning Fast Search Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `localhost`, `movies`, `search` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Filtering & Facets` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `indexes`.
2. **Input normalization**: shape incoming data so `curl` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `http`.
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
- search upstream code for `indexes` and `curl` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Typo Tolerance & Relevance](04-typo-tolerance-relevance.md)
- [Next Chapter: Chapter 6: Multi-Language Support](06-multi-language-support.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
