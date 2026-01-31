---
layout: default
title: "Chapter 2: AI Features & Configuration"
parent: "PhotoPrism Tutorial"
nav_order: 2
---

# Chapter 2: AI Features & Configuration

This chapter covers PhotoPrism's AI capabilities including TensorFlow integration, automatic tagging, and AI model configuration.

## 🧠 AI Engine Overview

### TensorFlow Integration

```bash
# PhotoPrism uses TensorFlow for AI features
# Models are automatically downloaded on first use
docker run -e PHOTOPRISM_DISABLE_TENSORFLOW=false photoprism/photoprism:latest
```

### AI Features

```typescript
// PhotoPrism's AI capabilities
const aiFeatures = {
  objectDetection: "Identify objects, scenes, and landmarks",
  facialRecognition: "Detect and recognize faces",
  imageClassification: "Categorize photos by content",
  colorDetection: "Analyze dominant colors",
  locationEstimation: "Estimate photo locations",
  autoTagging: "Generate descriptive tags"
}
```

## ⚙️ AI Configuration

### Environment Variables

```bash
# AI-related configuration
PHOTOPRISM_DISABLE_TENSORFLOW=false    # Enable TensorFlow
PHOTOPRISM_TF_MODEL_PATH=/photoprism/storage/models  # Model storage
PHOTOPRISM_DETECT_NSFW=false          # NSFW content detection
PHOTOPRISM_UPLOAD_NSFW=false          # Block NSFW uploads
```

### Model Management

```typescript
// Managing AI models
const modelConfig = {
  classification: {
    model: "nasnet",
    enabled: true,
    confidence: 0.1
  },
  facialRecognition: {
    model: "faceapi",
    enabled: true,
    minConfidence: 0.5
  },
  nsfw: {
    model: "nsfwjs",
    enabled: false,
    threshold: 0.8
  }
}
```

## 🎯 Object Detection

### Automatic Tagging

```typescript
// AI-generated tags examples
const aiTags = {
  scenes: ["landscape", "portrait", "street", "nature", "urban"],
  objects: ["car", "person", "dog", "cat", "building", "tree"],
  activities: ["sports", "dining", "travel", "party", "meeting"],
  weather: ["sunny", "cloudy", "rainy", "snowy"]
}
```

### Tag Management

```typescript
// Managing AI-generated tags
const tagManagement = {
  review: "Manually review and correct AI tags",
  blacklist: "Exclude unwanted tags",
  whitelist: "Only allow specific tags",
  synonyms: "Group similar tags together",
  priorities: "Set importance levels for tags"
}
```

## 👥 Facial Recognition

### Setup Process

```typescript
// Facial recognition workflow
const facialRecognitionSetup = [
  "Enable facial recognition in settings",
  "Upload photos with faces",
  "Wait for AI processing",
  "Review detected faces",
  "Assign names to faces",
  "Create face clusters"
]
```

### Face Clustering

```typescript
// Face clustering configuration
const faceClustering = {
  minConfidence: 0.8,
  maxDistance: 0.6,
  minClusterSize: 3,
  autoMerge: true,
  manualReview: true
}
```

## 🎨 Color Analysis

### Color Detection

```typescript
// Color analysis features
const colorAnalysis = {
  dominantColors: "Extract main colors from photos",
  colorPalette: "Generate color schemes",
  colorSearch: "Search by color similarity",
  colorMood: "Determine color mood/temperature"
}
```

## 📍 Location Estimation

### GPS and Location

```typescript
// Location features
const locationFeatures = {
  gpsExtraction: "Extract GPS data from photos",
  reverseGeocoding: "Convert coordinates to place names",
  locationSearch: "Search by location",
  mapView: "View photos on map",
  locationClustering: "Group photos by location"
}
```

## 🔧 Performance Tuning

### AI Processing Optimization

```bash
# Performance configuration
PHOTOPRISM_WORKERS=2                    # Number of workers
PHOTOPRISM_INDEX_WORKERS=1              # Index workers
PHOTOPRISM_FACE_WORKERS=1               # Face recognition workers
PHOTOPRISM_THUMB_WORKERS=2              # Thumbnail workers
```

### Resource Management

```typescript
// Resource allocation
const resourceConfig = {
  memory: {
    tensorflow: "2GB",
    indexing: "1GB",
    thumbnails: "512MB"
  },
  cpu: {
    workers: 4,
    priority: "background"
  },
  storage: {
    models: "/photoprism/storage/models",
    cache: "/photoprism/storage/cache"
  }
}
```

## 📊 AI Analytics

### Processing Statistics

```typescript
// AI processing metrics
const aiMetrics = {
  totalProcessed: 0,
  averageProcessingTime: 0,
  successRate: 0,
  tagAccuracy: 0,
  faceRecognitionRate: 0
}
```

## 🚨 Troubleshooting AI Issues

### Common Problems

1. **TensorFlow Not Working**
   ```bash
   # Check TensorFlow status
   docker logs photoprism | grep tensorflow

   # Ensure sufficient memory
   docker stats photoprism
   ```

2. **Slow Processing**
   ```bash
   # Increase workers
   PHOTOPRISM_WORKERS=4

   # Check CPU usage
   docker stats
   ```

3. **Inaccurate Tags**
   ```bash
   # Adjust confidence threshold
   PHOTOPRISM_AI_CONFIDENCE=0.2

   # Review and correct tags manually
   ```

## 📝 Chapter Summary

- ✅ Configured TensorFlow integration
- ✅ Set up automatic tagging and object detection
- ✅ Enabled facial recognition features
- ✅ Configured color analysis
- ✅ Optimized AI processing performance
- ✅ Troubleshot common AI issues

**Key Takeaways:**
- AI features require TensorFlow and sufficient resources
- Processing happens automatically in background
- Manual review improves AI accuracy over time
- Performance can be tuned based on hardware
- AI models are downloaded automatically on first use
