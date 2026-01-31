---
layout: default
title: "Chapter 4: Typo Tolerance & Relevance"
parent: "MeiliSearch Tutorial"
nav_order: 4
---

# Chapter 4: Typo Tolerance & Relevance

This chapter dives deep into Meilisearch's typo tolerance system and how to customize search relevance for your use case.

## 🎯 Typo Tolerance System

### How It Works

Meilisearch's typo tolerance system automatically corrects spelling mistakes:

```bash
# Original: "shwshank" → Corrected: "shawshank"
curl 'http://localhost:7700/indexes/movies/search?q=shwshank'

# Original: "str wr" → Corrected: "star war"
curl 'http://localhost:7700/indexes/movies/search?q=str wr'
```

### Typo Tolerance Levels

```javascript
// Configuration for typo tolerance
{
  "minWordSizeForTypos": {
    "oneTypo": 5,    // Words ≥5 chars: 1 typo allowed
    "twoTypos": 9    // Words ≥9 chars: 2 typos allowed
  }
}
```

**Examples:**
- "shawshank" (9 chars) → Allows 2 typos: "shwshnk", "shawshnck"
- "star" (4 chars) → Allows 0 typos: exact match only
- "inception" (9 chars) → Allows 2 typos: "insption", "incepshun"

## ⚙️ Configuring Typo Tolerance

### Basic Configuration

```bash
curl -X PUT 'http://localhost:7700/indexes/movies/settings/typo-tolerance' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "enabled": true,
    "minWordSizeForTypos": {
      "oneTypo": 5,
      "twoTypos": 9
    },
    "disableOnAttributes": ["id"],
    "disableOnWords": ["nolan"]
  }'
```

### Disable Typo Tolerance

```bash
# Disable completely
curl -X PUT 'http://localhost:7700/indexes/movies/settings/typo-tolerance' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{"enabled": false}'
```

### Attribute-Specific Settings

```bash
# Disable typo tolerance for specific attributes
curl -X PUT 'http://localhost:7700/indexes/movies/settings/typo-tolerance' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "disableOnAttributes": ["director", "year"]
  }'
```

## 🎨 Search Relevance

### Ranking Rules

Meilisearch uses a sophisticated ranking system:

```bash
# Default ranking rules
curl 'http://localhost:7700/indexes/movies/settings/ranking-rules'
```

**Default Rules:**
```json
[
  "words",        // Number of query words in document
  "typo",         // Typo penalty
  "proximity",    // Word proximity in document
  "attribute",    // Field importance
  "sort",         // Custom sort order
  "exactness"     // Exact word matches
]
```

### Custom Ranking Rules

```bash
curl -X PUT 'http://localhost:7700/indexes/movies/settings/ranking-rules' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "words",
    "typo",
    "proximity",
    "attribute",
    "sort",
    "exactness",
    "release_date:desc"
  ]'
```

### Attribute Ranking

```bash
# Define attribute importance
curl -X PUT 'http://localhost:7700/indexes/movies/settings/searchable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "title",       // Most important
    "director",    // Second
    "genre",       // Third
    "description"  // Least important
  ]'
```

## 🔍 Relevance Tuning

### Stop Words

```bash
# Configure stop words
curl -X PUT 'http://localhost:7700/indexes/movies/settings/stop-words' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '["the", "a", "an", "and", "or", "but"]'
```

### Synonyms

```bash
# Add synonyms
curl -X PUT 'http://localhost:7700/indexes/movies/settings/synonyms' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "movie": ["film", "picture", "motion picture"],
    "sci-fi": ["science fiction", "scifi"],
    "thriller": ["suspense", "mystery"]
  }'
```

## 📊 Understanding Search Scores

### Debug Search

```bash
# Enable ranking score details (experimental)
curl 'http://localhost:7700/indexes/movies/search?q=shawshank&showRankingScore=true'
```

**Response with ranking details:**
```json
{
  "hits": [
    {
      "_rankingScore": 0.85,
      "_rankingScoreDetails": {
        "words": { "order": 0, "matchingWords": 1, "maxMatchingWords": 1, "score": 1.0 },
        "typo": { "order": 1, "typoCount": 2, "score": 0.8 },
        "proximity": { "order": 2, "score": 0.9 }
      }
    }
  ]
}
```

## 🎯 Advanced Relevance Features

### Custom Sort

```bash
# Sort by custom criteria
curl 'http://localhost:7700/indexes/movies/search?q=movie&sort=rating:desc,year:desc'
```

### Boosting

```bash
# Use attribute ranking for boosting
curl -X PUT 'http://localhost:7700/indexes/movies/settings/searchable-attributes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "title",
    "title",
    "title",        // Boost title matches
    "director",
    "description"
  ]'
```

### Exact Match Boost

```bash
# Configure exactness ranking
curl -X PUT 'http://localhost:7700/indexes/movies/settings/ranking-rules' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "exactness",   // Prioritize exact matches
    "words",
    "typo",
    "proximity"
  ]'
```

## 🌍 Multi-Language Support

### Language Detection

```bash
# Meilisearch automatically detects language
curl 'http://localhost:7700/indexes/movies/search?q=film'   # English
curl 'http://localhost:7700/indexes/movies/search?q=película'  # Spanish
```

### Language-Specific Settings

```bash
# Configure language-specific stop words
curl -X PUT 'http://localhost:7700/indexes/movies/settings/stop-words' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "the", "a", "an",     // English
    "el", "la", "los"     // Spanish
  ]'
```

## 📈 Performance Optimization

### Relevance vs Speed

```javascript
// Balance relevance and performance
const searchConfig = {
  // High relevance (slower)
  rankingRules: [
    "words", "typo", "proximity", "attribute", "sort", "exactness"
  ],

  // Fast search (less relevant)
  rankingRules: [
    "words", "attribute"
  ]
};
```

### Index Optimization

```bash
# Optimize index for search
curl -X POST 'http://localhost:7700/indexes/movies/optimize' \
  -H 'Authorization: Bearer your_master_key'
```

## 🎯 Relevance Testing

### A/B Testing Setup

```javascript
// Test different ranking configurations
async function testRelevance(configA, configB, queries) {
  const results = [];

  for (const query of queries) {
    const resultA = await search(query, configA);
    const resultB = await search(query, configB);

    results.push({
      query,
      configA: resultA.hits.slice(0, 5),
      configB: resultB.hits.slice(0, 5)
    });
  }

  return results;
}
```

### Relevance Metrics

```javascript
// Calculate relevance metrics
function calculateMetrics(results, relevantDocs) {
  let precision = 0;
  let recall = 0;

  results.forEach(result => {
    const relevant = result.filter(doc => relevantDocs.includes(doc.id));
    precision += relevant.length / result.length;
    recall += relevant.length / relevantDocs.length;
  });

  return {
    precision: precision / results.length,
    recall: recall / results.length,
    f1Score: 2 * (precision * recall) / (precision + recall)
  };
}
```

## 🚨 Troubleshooting Relevance

### Common Issues

1. **Irrelevant Results**
   ```bash
   # Check ranking rules
   curl 'http://localhost:7700/indexes/movies/settings/ranking-rules'

   # Adjust searchable attributes order
   curl -X PUT 'http://localhost:7700/indexes/movies/settings/searchable-attributes' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer your_master_key' \
     --data '["title", "description"]'
   ```

2. **Typo Tolerance Too Aggressive**
   ```bash
   # Reduce typo tolerance
   curl -X PUT 'http://localhost:7700/indexes/movies/settings/typo-tolerance' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer your_master_key' \
     --data '{"minWordSizeForTypos": {"oneTypo": 8, "twoTypos": 12}}'
   ```

## 📝 Chapter Summary

- ✅ Configured typo tolerance settings
- ✅ Customized ranking rules for relevance
- ✅ Added synonyms and stop words
- ✅ Optimized search performance
- ✅ Tested and measured relevance
- ✅ Troubleshot common relevance issues

**Key Takeaways:**
- Typo tolerance improves user experience
- Ranking rules control result relevance
- Attribute order affects search importance
- Synonyms expand search coverage
- Regular relevance testing ensures quality
