---
layout: default
title: "Chapter 5: Facial Recognition"
parent: "PhotoPrism Tutorial"
nav_order: 5
---

# Chapter 5: Facial Recognition

This chapter covers PhotoPrism's facial recognition capabilities for identifying and organizing people in your photos.

## 👥 Setting Up Facial Recognition

### Enable Facial Recognition

```bash
# Enable facial recognition in environment
PHOTOPRISM_DISABLE_FACES=false
PHOTOPRISM_FACE_WORKERS=1

# Or through web interface
# Settings > AI > Enable Facial Recognition
```

### Processing Photos

```typescript
// Facial recognition workflow
const facialRecognitionProcess = [
  "Upload photos with faces",
  "Wait for AI processing",
  "Review detected faces",
  "Assign names to faces",
  "Create person entries",
  "Merge duplicate faces"
]
```

## 🔍 Face Detection

### Automatic Detection

```typescript
// Face detection configuration
const faceDetectionConfig = {
  minConfidence: 0.5,      // Minimum detection confidence
  minFaceSize: 20,         // Minimum face size in pixels
  maxFacesPerPhoto: 10,    // Maximum faces to detect
  detectAngles: true,      // Detect faces at angles
  detectOcclusions: true   // Handle partial occlusions
}
```

### Detection Results

```typescript
// Face detection output
const detectionResults = {
  faceId: "face_12345",
  confidence: 0.87,
  boundingBox: {
    x: 100, y: 150,
    width: 80, height: 100
  },
  landmarks: {
    leftEye: [120, 170],
    rightEye: [150, 170],
    nose: [135, 185],
    mouth: [135, 200]
  }
}
```

## 🏷️ Face Naming and Organization

### Assigning Names

```typescript
// Name assignment process
const namingProcess = {
  selectFace: "Click on detected face",
  enterName: "Type person's name",
  confirmMatch: "Confirm face matches person",
  createPerson: "Create new person entry",
  mergeFaces: "Merge similar faces"
}
```

### Person Management

```typescript
// Managing people in your library
const personManagement = {
  create: "Create new person entries",
  edit: "Edit person names and details",
  merge: "Merge duplicate person entries",
  delete: "Remove person entries",
  hide: "Hide sensitive person entries",
  export: "Export person data"
}
```

## 📊 Face Clustering

### Automatic Clustering

```typescript
// Face clustering settings
const clusteringConfig = {
  enabled: true,
  minClusterSize: 3,
  maxDistance: 0.6,
  autoMerge: true,
  manualReview: false
}
```

### Cluster Management

```typescript
// Managing face clusters
const clusterManagement = {
  reviewClusters: "Review AI-generated clusters",
  splitClusters: "Split incorrectly grouped faces",
  mergeClusters: "Merge related face clusters",
  renameClusters: "Assign names to clusters",
  deleteClusters: "Remove unwanted clusters"
}
```

## 🔍 Searching by People

### Person-Based Search

```typescript
// Search queries for people
const personSearchQueries = [
  "photos of John",
  "pictures with Mary",
  "family photos",
  "selfies",
  "group photos with Sarah",
  "photos without people"
]
```

### Advanced Person Filters

```typescript
// Complex person-based filters
const personFilters = {
  specificPerson: "photos of John Smith",
  multiplePeople: "photos with John AND Mary",
  groups: "photos with 3 or more people",
  unnamed: "photos with unrecognized faces",
  excluded: "photos without specific person"
}
```

## 📈 Recognition Accuracy

### Improving Accuracy

```typescript
// Accuracy improvement techniques
const accuracyImprovements = {
  morePhotos: "Add more photos of each person",
  betterQuality: "Use higher quality face photos",
  variedAngles: "Include photos from different angles",
  manualCorrections: "Manually correct misidentifications",
  regularUpdates: "Update face models regularly"
}
```

### Performance Metrics

```typescript
// Facial recognition metrics
const recognitionMetrics = {
  detectionRate: 0.92,     // Faces detected / total faces
  recognitionAccuracy: 0.85, // Correct identifications
  falsePositiveRate: 0.03,  // Incorrect identifications
  processingTime: 2.1       // Seconds per photo
}
```

## 🔒 Privacy Considerations

### Privacy Settings

```typescript
// Privacy and security settings
const privacySettings = {
  faceDetection: "Enable/disable face detection",
  faceStorage: "Store face embeddings locally",
  dataSharing: "Never share face data externally",
  accessControl: "Control who can view face data",
  anonymization: "Option to anonymize faces"
}
```

### Data Protection

```typescript
// Protecting facial recognition data
const dataProtection = {
  localStorage: "All data stored locally",
  encryption: "Encrypt face embeddings",
  accessLogging: "Log access to face data",
  backupSecurity: "Secure face data backups",
  deletion: "Complete data deletion options"
}
```

## 🚀 Performance Optimization

### Processing Optimization

```bash
# Optimize facial recognition performance
PHOTOPRISM_FACE_WORKERS=2
PHOTOPRISM_WORKERS=4
PHOTOPRISM_INDEX_WORKERS=2
```

### Hardware Acceleration

```typescript
// Hardware acceleration options
const hardwareAcceleration = {
  cpu: "Standard CPU processing",
  gpu: "GPU acceleration (if available)",
  tpu: "Tensor Processing Unit (advanced)",
  distributed: "Distributed processing"
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Faces Not Detected**
   ```bash
   # Check face detection settings
   PHOTOPRISM_DISABLE_FACES=false

   # Review photo quality
   # Ensure good lighting and clear faces
   ```

2. **Incorrect Recognition**
   ```bash
   # Add more photos of the person
   # Manually correct misidentifications
   # Check photo quality and angles
   ```

3. **Slow Processing**
   ```bash
   # Increase face workers
   PHOTOPRISM_FACE_WORKERS=2

   # Check available resources
   docker stats
   ```

## 📊 Analytics and Insights

### Usage Statistics

```typescript
// Facial recognition analytics
const faceAnalytics = {
  totalFaces: 1250,
  namedPeople: 45,
  unnamedFaces: 234,
  recognitionRate: 0.89,
  processingTime: "2.3 seconds per photo"
}
```

### Person Insights

```typescript
// Insights about people in photos
const personInsights = {
  mostPhotographed: "John (150 photos)",
  recentActivity: "Mary last appeared 3 days ago",
  groupFrequency: "Family photos: 25% of collection",
  locationPatterns: "Sarah often photographed at beach"
}
```

## 📝 Chapter Summary

- ✅ Enabled and configured facial recognition
- ✅ Processed photos for face detection
- ✅ Assigned names to detected faces
- ✅ Managed face clusters and person entries
- ✅ Searched photos by people
- ✅ Improved recognition accuracy
- ✅ Configured privacy and security settings

**Key Takeaways:**
- Facial recognition requires good quality photos
- Manual review improves accuracy over time
- Privacy settings protect sensitive data
- Performance can be optimized with hardware
- Regular maintenance improves results
- Face data is stored locally and securely
