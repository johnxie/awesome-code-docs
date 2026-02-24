---
layout: default
title: "Chapter 1: Getting Started with PhotoPrism"
parent: "PhotoPrism Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with PhotoPrism

Welcome to PhotoPrism! In this chapter, we'll install PhotoPrism, set up your first photo library, and explore the basic features.

## 🚀 Installation Options

### Docker Installation (Recommended)

```bash
# Create directories for photos and storage
mkdir -p ~/photoprism/photos ~/photoprism/storage

# Run PhotoPrism with Docker
docker run -d \
  --name photoprism \
  -p 2342:2342 \
  -e PHOTOPRISM_ADMIN_PASSWORD="your-secure-password" \
  -e PHOTOPRISM_SITE_TITLE="My Photo Library" \
  -e PHOTOPRISM_SITE_DESCRIPTION="Personal photo collection" \
  -v ~/photoprism/photos:/photoprism/photos \
  -v ~/photoprism/storage:/photoprism/storage \
  photoprism/photoprism:latest

# Check if container is running
docker ps
```

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  photoprism:
    image: photoprism/photoprism:latest
    container_name: photoprism
    restart: unless-stopped
    ports:
      - "2342:2342"
    environment:
      PHOTOPRISM_ADMIN_PASSWORD: "your-secure-password"
      PHOTOPRISM_SITE_TITLE: "My Photo Library"
      PHOTOPRISM_SITE_DESCRIPTION: "Personal photo collection"
      PHOTOPRISM_DATABASE_DRIVER: "sqlite"
      PHOTOPRISM_HTTP_HOST: "0.0.0.0"
      PHOTOPRISM_HTTP_PORT: 2342
    volumes:
      - "./photos:/photoprism/photos"
      - "./storage:/photoprism/storage"
    networks:
      - photoprism_network

networks:
  photoprism_network:
    driver: bridge
```

### Manual Installation

```bash
# Download the latest release
wget https://github.com/photoprism/photoprism/releases/download/v231203/photoprism_231203_linux_amd64.tar.gz

# Extract and install
tar -xzf photoprism_*.tar.gz
sudo mv photoprism /usr/local/bin/

# Create user and directories
sudo useradd -m -s /bin/bash photoprism
sudo mkdir -p /var/lib/photoprism/{photos,storage}
sudo chown -R photoprism:photoprism /var/lib/photoprism

# Create systemd service
sudo tee /etc/systemd/system/photoprism.service > /dev/null <<EOF
[Unit]
Description=PhotoPrism
After=network.target

[Service]
Type=simple
User=photoprism
Group=photoprism
WorkingDirectory=/var/lib/photoprism
ExecStart=/usr/local/bin/photoprism start
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start the service
sudo systemctl enable photoprism
sudo systemctl start photoprism
```

## ⚙️ Initial Configuration

### Accessing PhotoPrism

```bash
# Open your browser and navigate to:
echo "http://localhost:2342"

# Or if running on a server:
echo "http://your-server-ip:2342"
```

### First Login

```typescript
// Default admin credentials
const defaultCredentials = {
  username: "admin",
  password: process.env.PHOTOPRISM_ADMIN_PASSWORD // Set during installation
}

// Change password after first login
```

### Basic Settings

```typescript
// Essential settings to configure
const initialSettings = {
  site: {
    title: "My Photo Library",
    description: "Personal photo collection",
    caption: "Powered by PhotoPrism"
  },
  library: {
    path: "/photoprism/photos",
    originalsPath: "/photoprism/photos",
    importPath: "/photoprism/photos/import"
  },
  features: {
    upload: true,
    download: true,
    share: true,
    archive: true
  }
}
```

## 📸 Adding Your First Photos

### File Upload

```bash
# Copy photos to the mounted directory
cp ~/my-photos/*.jpg ~/photoprism/photos/

# Or use the web interface upload
# 1. Go to Library > Upload
# 2. Drag and drop photos or click to select
# 3. Click "Upload" to start
```

### Directory Structure

```bash
# Recommended organization
photoprism/photos/
├── 2023/
│   ├── 01-January/
│   │   ├── vacation/
│   │   ├── family/
│   │   └── events/
│   ├── 02-February/
│   └── ...
├── 2024/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
└── import/          # For new photos to be processed
```

### Supported Formats

```typescript
// PhotoPrism supports:
const supportedFormats = {
  images: [
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif',
    'webp', 'heic', 'heif', 'dng', 'arw', 'cr2', 'cr3',
    'nef', 'nrw', 'orf', 'raf', 'rw2', 'srw'
  ],
  videos: [
    'mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v', 'mpg', 'mpeg'
  ],
  raw: [
    'dng', 'arw', 'cr2', 'cr3', 'nef', 'nrw', 'orf', 'raf', 'rw2', 'srw'
  ]
}
```

## 🔍 Exploring the Interface

### Main Navigation

```typescript
// Key sections of PhotoPrism
const navigationSections = {
  browse: "View and explore your photos",
  search: "Advanced search functionality",
  library: "Manage your photo library",
  albums: "Create and manage albums",
  labels: "View AI-generated labels",
  people: "Facial recognition results",
  places: "Location-based organization"
}
```

### Photo View

```typescript
// Photo details view includes:
const photoDetails = {
  metadata: {
    dateTaken: "2023-12-25 14:30:00",
    camera: "Canon EOS R5",
    lens: "RF 24-70mm f/2.8L IS USM",
    exposure: "1/200 sec",
    aperture: "f/8",
    iso: 100
  },
  aiLabels: [
    "landscape", "mountain", "sky", "nature", "outdoor"
  ],
  location: {
    latitude: 46.516,
    longitude: 8.129,
    place: "Jungfraujoch, Switzerland"
  }
}
```

## 🎯 Basic Features

### Photo Actions

```typescript
// Available actions for photos
const photoActions = {
  view: "Open full-size image",
  edit: "Edit metadata and labels",
  download: "Download original file",
  share: "Generate shareable link",
  archive: "Move to archive",
  delete: "Remove from library",
  favorite: "Mark as favorite"
}
```

### Quick Search

```bash
# Basic search examples
search_queries = [
    "mountains",      # Search for photos with mountains
    "2023",          # Photos from 2023
    "vacation",      # Photos labeled as vacation
    "sunset",        # Photos with sunset scenes
    "portrait"       # Portrait-oriented photos
]
```

## 📊 Library Statistics

### Getting Started Metrics

```typescript
// Check your library status
const libraryStats = {
  totalPhotos: 0,
  totalVideos: 0,
  storageUsed: "0 GB",
  indexedPhotos: 0,
  aiProcessed: 0
}

// View in Settings > Library
```

## 🚨 Troubleshooting

### Common Issues

1. **Container Won't Start**
   ```bash
   # Check Docker logs
   docker logs photoprism

   # Common issues:
   # - Port 2342 already in use
   # - Insufficient permissions
   # - Invalid volume paths
   ```

2. **Cannot Access Web Interface**
   ```bash
   # Check if service is running
   docker ps | grep photoprism

   # Check port binding
   netstat -tlnp | grep 2342

   # Firewall issues
   sudo ufw allow 2342
   ```

3. **Photos Not Appearing**
   ```bash
   # Check file permissions
   ls -la ~/photoprism/photos/

   # Check container logs for indexing errors
   docker logs photoprism | grep -i error

   # Manual re-index
   docker exec photoprism photoprism index
   ```

4. **Memory Issues**
   ```bash
   # Increase Docker memory limit
   docker run --memory=4g --memory-swap=8g ...

   # Or in docker-compose.yml
   services:
     photoprism:
       deploy:
         resources:
           limits:
             memory: 4G
           reservations:
             memory: 1G
   ```

## 📊 Performance Tuning

### Basic Optimization

```yaml
# Optimized docker-compose.yml
version: '3.8'
services:
  photoprism:
    image: photoprism/photoprism:latest
    environment:
      PHOTOPRISM_WORKERS: 2          # Number of workers
      PHOTOPRISM_INDEX_WORKERS: 1    # Index workers
      PHOTOPRISM_THUMB_FILTER: "lanczos"  # Better quality thumbnails
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 1G
```

## 🎯 Next Steps

In the next chapter, we'll explore PhotoPrism's AI features and how to configure TensorFlow integration for automatic photo tagging and object recognition.

## 📝 Chapter Summary

- ✅ Installed PhotoPrism using Docker or manual installation
- ✅ Configured initial settings and admin access
- ✅ Added first photos to the library
- ✅ Explored the web interface and basic features
- ✅ Troubleshot common setup issues
- ✅ Optimized basic performance settings

**Key Takeaways:**
- Docker installation is the easiest way to get started
- Proper directory structure helps with organization
- PhotoPrism supports a wide range of photo formats
- Web interface is intuitive and feature-rich
- Basic troubleshooting helps resolve common issues
- Performance can be tuned based on your hardware

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `photoprism`, `photos`, `docker` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with PhotoPrism` as an operating subsystem inside **PhotoPrism Tutorial: AI-Powered Photos App**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `sudo`, `storage`, `your` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with PhotoPrism` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `photoprism`.
2. **Input normalization**: shape incoming data so `photos` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `docker`.
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
- search upstream code for `photoprism` and `photos` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: AI Features & Configuration](02-ai-features-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
