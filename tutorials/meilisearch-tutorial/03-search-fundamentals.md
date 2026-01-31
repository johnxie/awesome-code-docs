---
layout: default
title: "Chapter 3: Search Fundamentals"
parent: "MeiliSearch Tutorial"
nav_order: 3
---

# Chapter 3: Search Fundamentals

This chapter covers the core search capabilities of Meilisearch, from basic queries to advanced search features.

## 🔍 Basic Search

### Simple Text Search

```bash
# Basic search
curl 'http://localhost:7700/indexes/movies/search?q=star'

# Search with multiple words
curl 'http://localhost:7700/indexes/movies/search?q=star wars'
```

### Exact Phrase Search

```bash
# Search for exact phrase
curl 'http://localhost:7700/indexes/movies/search?q="star wars"'
```

### Field-Specific Search

```bash
# Note: Meilisearch searches all searchable fields by default
# To search specific fields, use filters
curl 'http://localhost:7700/indexes/movies/search?q=nolan&filter=director=Nolan'
```

## 🎯 Search Parameters

### Limit and Offset

```bash
# Get first 5 results
curl 'http://localhost:7700/indexes/movies/search?q=movie&limit=5'

# Pagination
curl 'http://localhost:7700/indexes/movies/search?q=movie&limit=10&offset=20'
```

### Sorting Results

```bash
# Sort by year (ascending)
curl 'http://localhost:7700/indexes/movies/search?q=movie&sort=year:asc'

# Sort by rating (descending)
curl 'http://localhost:7700/indexes/movies/search?q=movie&sort=rating:desc'

# Multiple sort criteria
curl 'http://localhost:7700/indexes/movies/search?q=movie&sort=rating:desc,year:asc'
```

### Matching Strategy

```bash
# Last word takes precedence (default)
curl 'http://localhost:7700/indexes/movies/search?q=star wars&matchingStrategy=last'

# All words must match
curl 'http://localhost:7700/indexes/movies/search?q=star wars&matchingStrategy=all'
```

## 🔤 Typo Tolerance

Meilisearch automatically handles typos and spelling mistakes:

```bash
# Original query
curl 'http://localhost:7700/indexes/movies/search?q=shwshnk'

# Still finds "Shawshank"
# Meilisearch corrects up to 2 typos for words with 5+ characters
```

### Typo Tolerance Configuration

```bash
# Configure typo tolerance
curl -X PUT 'http://localhost:7700/indexes/movies/settings/typo-tolerance' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "enabled": true,
    "minWordSizeForTypos": {
      "oneTypo": 5,
      "twoTypos": 9
    },
    "disableOnAttributes": ["director"]
  }'
```

## 🎨 Highlighting and Snippets

### Highlighting Search Terms

```bash
# Enable highlighting
curl 'http://localhost:7700/indexes/movies/search?q=star&attributesToHighlight=["title"]'
```

**Response with highlighting:**
```json
{
  "hits": [
    {
      "id": 1,
      "title": "Star Wars",
      "_formatted": {
        "title": "<em>Star</em> <em>Wars</em>"
      }
    }
  ]
}
```

### Custom Highlight Tags

```bash
curl 'http://localhost:7700/indexes/movies/search?q=star&highlightPreTag=<strong>&highlightPostTag=</strong>'
```

### Snippets

```bash
# Generate snippets for long text fields
curl 'http://localhost:7700/indexes/movies/search?q=space&attributesToSnippet=["description:50"]'
```

## 🔍 Advanced Search Features

### Placeholder Search

```bash
# Search for documents containing the word "space"
curl 'http://localhost:7700/indexes/movies/search?q=space'

# Use underscore for single character wildcard
curl 'http://localhost:7700/indexes/movies/search?q=sp_ce'
```

### Prefix Search

Meilisearch supports prefix search automatically:

```bash
# Finds "Star Wars", "Star Trek", etc.
curl 'http://localhost:7700/indexes/movies/search?q=star'
```

### Multi-Language Support

```bash
# Meilisearch handles different languages automatically
curl 'http://localhost:7700/indexes/movies/search?q=film'  # English
curl 'http://localhost:7700/indexes/movies/search?q=película'  # Spanish
```

## 📊 Search Analytics

### Searchable Attributes

```bash
# Configure which fields are searchable
curl -X PUT 'http://localhost:7700/indexes/movies/settings/searchable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["title", "director", "genre", "description"]'
```

### Ranking Rules

```bash
# Configure ranking rules
curl -X PUT 'http://localhost:7700/indexes/movies/settings/ranking-rules' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "words",
    "typo",
    "proximity",
    "attribute",
    "sort",
    "exactness"
  ]'
```

## 🔧 Search Performance

### Query Optimization

```bash
# Use specific queries instead of broad searches
curl 'http://localhost:7700/indexes/movies/search?q="exact phrase"'

# Use filters to narrow down results
curl 'http://localhost:7700/indexes/movies/search?q=movie&filter=year>=2000'
```

### Caching

```bash
# Meilisearch automatically caches frequent queries
# Cache can be cleared if needed
curl -X POST 'http://localhost:7700/indexes/movies/cache/clear' \
  -H 'Authorization: Bearer your_master_key'
```

## 📈 Faceted Search

### Basic Facets

```bash
# Enable facets
curl 'http://localhost:7700/indexes/movies/search?q=movie&facets=["genre","year"]'
```

**Response:**
```json
{
  "hits": [...],
  "facetDistribution": {
    "genre": {
      "Drama": 15,
      "Action": 12,
      "Comedy": 8
    },
    "year": {
      "2020": 5,
      "2019": 8,
      "2018": 10
    }
  }
}
```

## 🎯 Search Best Practices

### Query Construction

```javascript
// Good: Specific queries
const searchParams = {
  q: 'star wars',
  limit: 20,
  attributesToRetrieve: ['title', 'year', 'rating']
};

// Avoid: Overly broad queries
const badSearch = {
  q: 'a',  // Too broad
  limit: 1000  // Too many results
};
```

### Result Processing

```javascript
// Process search results
function processResults(response) {
  const { hits, estimatedTotalHits, processingTimeMs } = response;

  console.log(`Found ${estimatedTotalHits} results in ${processingTimeMs}ms`);

  return hits.map(hit => ({
    id: hit.id,
    title: hit._formatted?.title || hit.title,
    highlights: hit._formatted
  }));
}
```

## 🚨 Common Search Issues

### No Results Found

```bash
# Check if index exists
curl 'http://localhost:7700/indexes'

# Check if documents are indexed
curl 'http://localhost:7700/indexes/movies/documents'

# Check searchable attributes
curl 'http://localhost:7700/indexes/movies/settings/searchable-attributes'
```

### Slow Search Performance

```bash
# Check index stats
curl 'http://localhost:7700/indexes/movies/stats'

# Monitor task queue
curl 'http://localhost:7700/tasks?statuses=processing'
```

## 📝 Chapter Summary

- ✅ Performed basic and advanced searches
- ✅ Configured typo tolerance and highlighting
- ✅ Used sorting, pagination, and filtering
- ✅ Implemented faceted search
- ✅ Optimized search performance
- ✅ Handled common search issues

**Key Takeaways:**
- Meilisearch provides instant, typo-tolerant search
- Configure searchable attributes for better relevance
- Use highlighting and snippets for better UX
- Monitor performance and optimize queries
- Facets help users refine their searches
