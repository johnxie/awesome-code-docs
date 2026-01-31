---
layout: default
title: "Chapter 3: Photo Management"
parent: "PhotoPrism Tutorial"
nav_order: 3
---

# Chapter 3: Photo Management

This chapter covers importing, organizing, and managing your photo collection in PhotoPrism.

## 📥 Importing Photos

### Batch Import

```bash
# Copy photos to import directory
cp ~/new-photos/*.jpg ~/photoprism/photos/import/

# Trigger import
docker exec photoprism photoprism import

# Or use web interface
# Library > Import > Select files
```

### Import Options

```typescript
// Import configuration
const importOptions = {
  moveFiles: true,        // Move vs copy files
  deleteAfterImport: false, // Delete originals
  skipDuplicates: true,   // Skip existing files
  createAlbums: true,     // Auto-create albums
  indexOnly: false        // Index without moving
}
```

## 📁 Organization

### Folder Structure

```bash
# Recommended organization
photos/
├── originals/           # Original files
├── import/             # New photos to import
├── 2023/
│   ├── 01-january/
│   │   ├── vacation/
│   │   ├── family/
│   │   └── events/
│   └── 02-february/
└── albums/             # Album-specific folders
```

### Automatic Organization

```typescript
// Auto-organization features
const autoOrganization = {
  byDate: "Organize by capture date",
  byLocation: "Group by GPS location",
  byEvent: "Cluster by events",
  byPerson: "Group by people",
  byAlbum: "Custom album organization"
}
```

## 🏷️ Metadata Management

### EXIF Data

```typescript
// Photo metadata
const photoMetadata = {
  basic: {
    dateTaken: "2023-12-25T14:30:00Z",
    camera: "Canon EOS R5",
    lens: "RF 24-70mm f/2.8L",
    dimensions: "6000x4000"
  },
  exposure: {
    shutterSpeed: "1/200",
    aperture: "f/8",
    iso: 100,
    focalLength: "35mm"
  },
  location: {
    latitude: 46.516,
    longitude: 8.129,
    altitude: 3454,
    placeName: "Jungfraujoch"
  }
}
```

### Editing Metadata

```typescript
// Metadata editing capabilities
const metadataEditing = {
  title: "Photo title/description",
  keywords: "Search keywords",
  location: "GPS coordinates and place names",
  date: "Capture date and time",
  camera: "Camera and lens information",
  rating: "Star rating (1-5)",
  color: "Color labels"
}
```

## 📸 Albums and Collections

### Creating Albums

```typescript
// Album management
const albumFeatures = {
  create: "Create new albums",
  addPhotos: "Add photos to albums",
  removePhotos: "Remove photos from albums",
  sort: "Sort photos in albums",
  share: "Share albums with others",
  download: "Download entire albums"
}
```

### Smart Albums

```typescript
// AI-powered smart albums
const smartAlbums = {
  recent: "Recently added photos",
  favorites: "Favorited photos",
  people: "Photos of specific people",
  places: "Photos from specific locations",
  tags: "Photos with specific tags",
  colors: "Photos with specific colors"
}
```

## ⭐ Favorites and Ratings

### Photo Rating System

```typescript
// Rating and favoriting
const ratingSystem = {
  favorites: "Heart/like photos",
  stars: "1-5 star rating system",
  colorLabels: "Color-coded labels",
  quality: "Quality assessment",
  flags: "Custom flags and markers"
}
```

## 🗂️ File Operations

### Bulk Operations

```typescript
// Bulk photo operations
const bulkOperations = {
  select: "Select multiple photos",
  move: "Move to different folders",
  copy: "Copy to albums",
  delete: "Delete multiple photos",
  edit: "Bulk metadata editing",
  export: "Export selected photos"
}
```

### File Management

```typescript
// File operations
const fileOperations = {
  view: "View photo details",
  download: "Download original files",
  share: "Generate share links",
  archive: "Move to archive",
  restore: "Restore from archive",
  duplicate: "Find and handle duplicates"
}
```

## 🔍 Quality Control

### Photo Quality Assessment

```typescript
// Quality analysis
const qualityControl = {
  resolution: "Check image resolution",
  compression: "Assess compression quality",
  sharpness: "Analyze image sharpness",
  exposure: "Check exposure levels",
  noise: "Detect image noise",
  duplicates: "Find duplicate photos"
}
```

## 📊 Library Statistics

### Collection Analytics

```typescript
// Library statistics
const libraryStats = {
  totalPhotos: 15420,
  totalVideos: 234,
  storageUsed: "256 GB",
  averageFileSize: "12 MB",
  oldestPhoto: "2015-03-15",
  newestPhoto: "2024-01-20",
  cameras: ["Canon EOS R5", "iPhone 15", "Sony A7R"],
  locations: ["Switzerland", "Japan", "USA", "France"]
}
```

## 🚀 Performance Optimization

### Indexing Optimization

```bash
# Optimize indexing performance
PHOTOPRISM_INDEX_WORKERS=2
PHOTOPRISM_THUMB_WORKERS=4
PHOTOPRISM_WORKERS=4
```

### Storage Optimization

```typescript
// Storage management
const storageOptimization = {
  compression: "Optimize storage with compression",
  thumbnails: "Generate optimized thumbnails",
  originals: "Preserve original quality",
  cleanup: "Remove unused files",
  deduplication: "Eliminate duplicates"
}
```

## 📝 Chapter Summary

- ✅ Imported photos using various methods
- ✅ Organized photos with folders and albums
- ✅ Managed metadata and EXIF data
- ✅ Created and managed albums
- ✅ Used rating and favoriting systems
- ✅ Performed bulk operations
- ✅ Analyzed photo quality and statistics

**Key Takeaways:**
- Import process can be automated
- Good folder structure improves organization
- Metadata editing enhances searchability
- Albums provide flexible grouping
- Quality control ensures good photo management
- Bulk operations save time with large collections
