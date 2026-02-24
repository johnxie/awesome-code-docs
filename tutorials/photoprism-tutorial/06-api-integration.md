---
layout: default
title: "Chapter 6: API Integration"
parent: "PhotoPrism Tutorial"
nav_order: 6
---

# Chapter 6: API Integration

Welcome to **Chapter 6: API Integration**. In this part of **PhotoPrism Tutorial: AI-Powered Photos App**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers using PhotoPrism's REST API for automation, integration with other services, and custom applications.

## 🌐 API Overview

### Authentication

```typescript
// API authentication
const apiAuth = {
  username: "admin",
  password: process.env.PHOTOPRISM_ADMIN_PASSWORD,
  baseURL: "http://localhost:2342/api/v1"
}
```

### Basic API Call

```bash
# Test API connection
curl -u admin:password http://localhost:2342/api/v1/photos
```

## 📸 Photo Operations

### List Photos

```typescript
// Get photos with filters
const getPhotos = async (filters = {}) => {
  const params = new URLSearchParams({
    count: 100,
    offset: 0,
    ...filters
  })

  const response = await fetch(`${apiAuth.baseURL}/photos?${params}`, {
    headers: {
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    }
  })

  return response.json()
}

// Usage
const recentPhotos = await getPhotos({ 
  year: 2024, 
  month: 1 
})
```

### Upload Photos

```typescript
// Upload new photos
const uploadPhotos = async (files) => {
  const formData = new FormData()
  
  files.forEach(file => {
    formData.append('files', file)
  })

  const response = await fetch(`${apiAuth.baseURL}/photos/upload`, {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: formData
  })

  return response.json()
}
```

### Photo Details

```typescript
// Get photo details
const getPhotoDetails = async (photoId) => {
  const response = await fetch(`${apiAuth.baseURL}/photos/${photoId}`, {
    headers: {
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    }
  })

  return response.json()
}
```

## 🏷️ Metadata Management

### Update Photo Metadata

```typescript
// Update photo information
const updatePhoto = async (photoId, updates) => {
  const response = await fetch(`${apiAuth.baseURL}/photos/${photoId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: JSON.stringify(updates)
  })

  return response.json()
}

// Example updates
const updates = {
  Title: "Vacation Photo",
  Description: "Beautiful sunset at the beach",
  Keywords: ["vacation", "beach", "sunset"],
  Favorite: true
}
```

## 📁 Album Management

### Create Album

```typescript
// Create new album
const createAlbum = async (albumData) => {
  const response = await fetch(`${apiAuth.baseURL}/albums`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: JSON.stringify({
      Title: albumData.title,
      Description: albumData.description,
      Filter: albumData.filter
    })
  })

  return response.json()
}
```

### Add Photos to Album

```typescript
// Add photos to album
const addPhotosToAlbum = async (albumId, photoIds) => {
  const response = await fetch(`${apiAuth.baseURL}/albums/${albumId}/photos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: JSON.stringify({
      photos: photoIds
    })
  })

  return response.json()
}
```

## 🔍 Search API

### Search Photos

```typescript
// Search photos via API
const searchPhotos = async (query, filters = {}) => {
  const params = new URLSearchParams({
    q: query,
    count: 50,
    ...filters
  })

  const response = await fetch(`${apiAuth.baseURL}/photos/search?${params}`, {
    headers: {
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    }
  })

  return response.json()
}

// Advanced search
const advancedSearch = await searchPhotos("mountains", {
  year: 2023,
  label: "landscape",
  geo: "46.516,8.129,10"  // lat,lng,radius
})
```

## 📊 Batch Operations

### Batch Update

```typescript
// Update multiple photos
const batchUpdate = async (photoIds, updates) => {
  const operations = photoIds.map(id => ({
    id,
    method: 'PUT',
    path: `/photos/${id}`,
    body: updates
  }))

  const response = await fetch(`${apiAuth.baseURL}/batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: JSON.stringify({ operations })
  })

  return response.json()
}
```

## 🔗 Webhook Integration

### Configure Webhooks

```typescript
// Set up webhooks for events
const configureWebhook = async (webhookConfig) => {
  const response = await fetch(`${apiAuth.baseURL}/webhooks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(`${apiAuth.username}:${apiAuth.password}`)
    },
    body: JSON.stringify({
      Url: webhookConfig.url,
      Events: webhookConfig.events,
      Method: webhookConfig.method || 'POST',
      Headers: webhookConfig.headers || {}
    })
  })

  return response.json()
}

// Example webhook for new photos
const photoWebhook = await configureWebhook({
  url: 'https://myapp.com/webhooks/photoprism',
  events: ['photo.create', 'photo.update'],
  headers: {
    'X-API-Key': 'my-api-key'
  }
})
```

## 📱 Mobile App Integration

### React Native Example

```typescript
// PhotoPrism React Native integration
import { useEffect, useState } from 'react'
import { View, Image, FlatList } from 'react-native'

const PhotoGallery = () => {
  const [photos, setPhotos] = useState([])

  useEffect(() => {
    fetchPhotos()
  }, [])

  const fetchPhotos = async () => {
    try {
      const response = await fetch('http://your-server:2342/api/v1/photos?count=20', {
        headers: {
          'Authorization': 'Basic ' + btoa('username:password')
        }
      })
      const data = await response.json()
      setPhotos(data)
    } catch (error) {
      console.error('Error fetching photos:', error)
    }
  }

  return (
    <FlatList
      data={photos}
      keyExtractor={(item) => item.ID}
      renderItem={({ item }) => (
        <Image 
          source={{ uri: item.ThumbnailUrl }} 
          style={{ width: 100, height: 100 }} 
        />
      )}
    />
  )
}
```

## 🚀 Automation Examples

### Automated Backup

```typescript
// Automated photo backup script
const backupPhotos = async () => {
  const photos = await getPhotos({ 
    year: new Date().getFullYear() 
  })

  for (const photo of photos) {
    const downloadUrl = `${apiAuth.baseURL}/photos/${photo.ID}/download`
    
    // Download and backup photo
    await downloadFile(downloadUrl, `./backup/${photo.ID}.jpg`)
  }
}
```

### Social Media Integration

```typescript
// Post photos to social media
const postToSocialMedia = async (photoId, platforms) => {
  const photo = await getPhotoDetails(photoId)
  
  for (const platform of platforms) {
    switch (platform) {
      case 'twitter':
        await postToTwitter(photo)
        break
      case 'instagram':
        await postToInstagram(photo)
        break
    }
  }
}
```

## 🔒 Security Best Practices

### API Key Management

```typescript
// Secure API key handling
const secureApiConfig = {
  useHttps: true,
  rotateKeys: true,
  rateLimiting: true,
  ipWhitelist: ['192.168.1.0/24'],
  auditLogging: true
}
```

### Request Validation

```typescript
// Validate API requests
const validateApiRequest = (req) => {
  const { query, filters } = req

  // Sanitize inputs
  const sanitizedQuery = sanitizeString(query)
  const validatedFilters = validateFilters(filters)

  return { sanitizedQuery, validatedFilters }
}
```

## 📊 API Analytics

### Usage Tracking

```typescript
// Track API usage
const apiAnalytics = {
  requestCount: 0,
  errorCount: 0,
  popularEndpoints: {},
  responseTimes: [],

  trackRequest(endpoint, responseTime, success) {
    this.requestCount++
    this.popularEndpoints[endpoint] = (this.popularEndpoints[endpoint] || 0) + 1
    this.responseTimes.push(responseTime)
    
    if (!success) this.errorCount++
  },

  getMetrics() {
    return {
      totalRequests: this.requestCount,
      errorRate: this.errorCount / this.requestCount,
      averageResponseTime: this.responseTimes.reduce((a, b) => a + b, 0) / this.responseTimes.length,
      popularEndpoints: Object.entries(this.popularEndpoints).sort((a, b) => b[1] - a[1])
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Authenticated with PhotoPrism API
- ✅ Performed CRUD operations on photos
- ✅ Managed metadata and albums
- ✅ Implemented search functionality
- ✅ Created batch operations
- ✅ Set up webhooks and integrations
- ✅ Built automation scripts
- ✅ Applied security best practices

**Key Takeaways:**
- REST API enables full automation
- Authentication uses Basic Auth
- Batch operations improve efficiency
- Webhooks enable real-time integration
- Security is critical for API access
- Analytics help monitor usage
- Integration enables custom workflows

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `apiAuth`, `photos`, `response` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: API Integration` as an operating subsystem inside **PhotoPrism Tutorial: AI-Powered Photos App**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `json`, `password`, `headers` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: API Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `apiAuth`.
2. **Input normalization**: shape incoming data so `photos` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `response`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [github.com/photoprism/photoprism](https://github.com/photoprism/photoprism)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism` (github.com).
- [github.com/photoprism/photoprism/discussions](https://github.com/photoprism/photoprism/discussions)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism/discussions` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `apiAuth` and `photos` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Facial Recognition](05-facial-recognition.md)
- [Next Chapter: Chapter 7: Backup & Migration](07-backup-migration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
