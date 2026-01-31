---
layout: default
title: "Chapter 6: Multi-Language Support"
parent: "MeiliSearch Tutorial"
nav_order: 6
---

# Chapter 6: Multi-Language Support

Meilisearch provides excellent support for multiple languages, making it perfect for international applications and global search experiences.

## 🌍 Language Detection

### Automatic Language Detection

```bash
# Meilisearch automatically detects language
curl 'http://localhost:7700/indexes/products/search?q=ordinateur'  # French
curl 'http://localhost:7700/indexes/products/search?q=computer'   # English
curl 'http://localhost:7700/indexes/products/search?q=computadora' # Spanish
```

### Supported Languages

Meilisearch supports 80+ languages including:
- **European**: English, French, German, Spanish, Italian, Portuguese
- **Asian**: Chinese, Japanese, Korean, Arabic, Hebrew
- **Others**: Russian, Hindi, Thai, Vietnamese, Turkish

## ⚙️ Language Configuration

### Stop Words

```bash
# Configure language-specific stop words
curl -X PUT 'http://localhost:7700/indexes/products/settings/stop-words' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    "the", "a", "an",        // English
    "le", "la", "les",       // French
    "el", "la", "los", "las" // Spanish
  ]'
```

### Synonyms

```bash
# Add multilingual synonyms
curl -X PUT 'http://localhost:7700/indexes/products/settings/synonyms' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "computer": ["ordinateur", "computadora", "computer", "电脑"],
    "phone": ["téléphone", "teléfono", "telefon", "电话"],
    "book": ["livre", "libro", "buch", "书"]
  }'
```

## 🎯 Localized Search

### Language-Specific Queries

```bash
# Search in different languages
curl 'http://localhost:7700/indexes/products/search?q=ordinateur'  # French for computer
curl 'http://localhost:7700/indexes/products/search?q=computadora' # Spanish for computer
curl 'http://localhost:7700/indexes/products/search?q=电脑'       # Chinese for computer
```

### Mixed Language Content

```javascript
// Handle documents with mixed languages
const mixedLanguageDoc = {
  id: 1,
  title: "iPhone 15 Pro",
  description: "Latest smartphone with advanced features",
  description_fr: "Dernier smartphone avec fonctionnalités avancées",
  description_es: "Último smartphone con características avanzadas",
  tags: ["smartphone", "apple", "technology"]
};
```

## 🔤 Character Handling

### Unicode Support

```bash
# Meilisearch handles Unicode characters
curl 'http://localhost:7700/indexes/products/search?q=café'     # French
curl 'http://localhost:7700/indexes/products/search?q=naïve'    # French
curl 'http://localhost:7700/indexes/products/search?q=北京'     # Chinese
```

### Diacritics Handling

```bash
# Search with or without diacritics
curl 'http://localhost:7700/indexes/products/search?q=cafe'   # Finds "café"
curl 'http://localhost:7700/indexes/products/search?q=café'   # Finds "café"
```

### Case Insensitive Search

```bash
# Case doesn't matter
curl 'http://localhost:7700/indexes/products/search?q=IPHONE'  # Finds "iPhone"
curl 'http://localhost:7700/indexes/products/search?q=iphone'  # Finds "iPhone"
```

## 📊 Language Analytics

### Language Distribution

```javascript
// Track search languages
const trackLanguageUsage = (query, language) => {
  analytics.track('search_language', {
    query: query,
    detectedLanguage: language,
    timestamp: new Date().toISOString()
  });
};
```

### Multi-Language Facets

```bash
# Facets work across languages
curl 'http://localhost:7700/indexes/products/search?q=phone&facets=["category","language"]'
```

## 🚀 International SEO

### Localized URLs

```javascript
// Handle localized search URLs
const localizedSearch = {
  '/en/search': { lang: 'en', q: 'computer' },
  '/fr/search': { lang: 'fr', q: 'ordinateur' },
  '/es/search': { lang: 'es', q: 'computadora' }
};
```

### Language-Specific Results

```javascript
// Return language-specific results
const getLocalizedResults = async (query, userLanguage) => {
  const filters = [`language=${userLanguage}`];
  const response = await search(query, { filter: filters });
  return response;
};
```

## 🎨 Advanced Features

### Language Boosting

```javascript
// Boost results in user's language
const boostLanguage = (results, userLanguage) => {
  return results.sort((a, b) => {
    const aLang = detectLanguage(a.title);
    const bLang = detectLanguage(b.title);

    if (aLang === userLanguage && bLang !== userLanguage) return -1;
    if (bLang === userLanguage && aLang !== userLanguage) return 1;
    return 0;
  });
};
```

### Fallback Languages

```javascript
// Fallback to English if no results in user's language
const searchWithFallback = async (query, primaryLang, fallbackLang = 'en') => {
  let results = await search(query, { filter: `language=${primaryLang}` });

  if (results.hits.length === 0) {
    results = await search(query, { filter: `language=${fallbackLang}` });
  }

  return results;
};
```

## 📱 Real-World Implementation

### E-commerce Example

```javascript
class MultilingualEcommerceSearch {
  constructor() {
    this.supportedLanguages = ['en', 'fr', 'es', 'de'];
  }

  async search(query, language) {
    // Configure search for specific language
    const filters = [`language=${language}`];
    const synonyms = await this.getLanguageSynonyms(language);

    return await this.performSearch(query, {
      filter: filters,
      synonyms: synonyms
    });
  }

  async getLanguageSynonyms(language) {
    // Load language-specific synonyms
    const synonymMap = {
      'fr': { 'computer': 'ordinateur', 'phone': 'téléphone' },
      'es': { 'computer': 'computadora', 'phone': 'teléfono' },
      'de': { 'computer': 'computer', 'phone': 'telefon' }
    };

    return synonymMap[language] || {};
  }
}
```

### Content Management System

```javascript
class MultilingualCMS {
  async indexContent(content, languages) {
    const documents = [];

    for (const lang of languages) {
      documents.push({
        id: `${content.id}_${lang}`,
        title: content.title[lang],
        content: content.content[lang],
        language: lang,
        tags: content.tags
      });
    }

    await this.indexDocuments(documents);
  }

  async search(query, language) {
    return await this.client.search(query, {
      filter: `language=${language}`,
      facets: ['tags', 'category']
    });
  }
}
```

## 🚀 Performance Optimization

### Language-Specific Indexes

```javascript
// Create separate indexes for each language
const createLanguageIndexes = async (baseName, languages) => {
  const indexes = {};

  for (const lang of languages) {
    const indexName = `${baseName}_${lang}`;
    indexes[lang] = await createIndex(indexName);

    // Configure language-specific settings
    await configureLanguageSettings(indexes[lang], lang);
  }

  return indexes;
};
```

### Caching Strategy

```javascript
// Cache language-specific search results
class LanguageSearchCache {
  constructor() {
    this.cache = new Map();
  }

  getKey(query, language) {
    return `${query}:${language}`;
  }

  async get(query, language) {
    const key = this.getKey(query, language);
    return this.cache.get(key);
  }

  async set(query, language, results) {
    const key = this.getKey(query, language);
    this.cache.set(key, results);
  }
}
```

## 🚨 Common Challenges

### Language Detection Issues

```javascript
// Handle ambiguous queries
const handleAmbiguousQuery = async (query) => {
  const possibleLanguages = detectPossibleLanguages(query);

  if (possibleLanguages.length > 1) {
    // Search in all possible languages
    const results = await Promise.all(
      possibleLanguages.map(lang => search(query, { filter: `language=${lang}` }))
    );

    return combineResults(results);
  }

  return await search(query);
};
```

### Mixed Content Handling

```javascript
// Handle documents with mixed language content
const processMixedContent = (document) => {
  const languages = detectLanguages(document.content);
  document.detectedLanguages = languages;
  document.primaryLanguage = languages[0];

  return document;
};
```

## 📊 Monitoring and Analytics

### Language Metrics

```javascript
// Track language usage
const languageAnalytics = {
  trackSearch(query, language, results) {
    analytics.track('multilingual_search', {
      query,
      language,
      resultCount: results.estimatedTotalHits,
      processingTime: results.processingTimeMs
    });
  },

  getLanguageStats() {
    return analytics.getMetrics('multilingual_search');
  }
};
```

## 📝 Best Practices

### Language Strategy

```javascript
const languageBestPractices = {
  // 1. Detect user's language preference
  detectUserLanguage: () => navigator.language || 'en',

  // 2. Provide language switcher
  showLanguageSwitcher: true,

  // 3. Fallback to primary language
  fallbackLanguage: 'en',

  // 4. Cache language-specific results
  enableCaching: true,

  // 5. Monitor language usage
  trackAnalytics: true
};
```

## 📝 Chapter Summary

- ✅ Configured multi-language support
- ✅ Handled Unicode and diacritics
- ✅ Implemented language-specific synonyms
- ✅ Built international search interfaces
- ✅ Optimized for global performance
- ✅ Monitored language usage analytics

**Key Takeaways:**
- Meilisearch supports 80+ languages automatically
- Configure language-specific stop words and synonyms
- Handle Unicode characters and diacritics properly
- Use language detection for better user experience
- Implement fallback strategies for better coverage
- Monitor and analyze language usage patterns
