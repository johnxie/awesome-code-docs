---
layout: default
title: "Chapter 1: Getting Started with Meilisearch"
parent: "MeiliSearch Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Meilisearch

Welcome to your Meilisearch journey! In this chapter, we'll get Meilisearch up and running and perform your first searches.

## 🚀 Installation

### Option 1: Download Binary

```bash
# Download the latest binary for your platform
curl -L https://install.meilisearch.com | sh

# Or download specific version
wget https://github.com/meilisearch/meilisearch/releases/download/v1.8.0/meilisearch-linux-amd64

# Make it executable
chmod +x meilisearch-linux-amd64
```

### Option 2: Docker

```bash
# Pull the official Docker image
docker pull getmeili/meilisearch:v1.8.0

# Run Meilisearch in Docker
docker run -p 7700:7700 getmeili/meilisearch:v1.8.0
```

### Option 3: Build from Source

```bash
# Clone the repository
git clone https://github.com/meilisearch/meilisearch.git
cd meilisearch

# Build with Cargo
cargo build --release
```

## ⚙️ Configuration

### Basic Configuration

```bash
# Start with default settings
./meilisearch

# Start with custom settings
./meilisearch --http-addr 127.0.0.1:7700 --master-key "your_master_key"
```

### Environment Variables

```bash
# Set environment variables
export MEILI_HTTP_ADDR=127.0.0.1:7700
export MEILI_MASTER_KEY=your_master_key
export MEILI_DB_PATH=./meili_data
export MEILI_ENV=production
```

### Configuration File

Create a `config.toml` file:

```toml
# Meilisearch configuration file
http_addr = "127.0.0.1:7700"
master_key = "your_master_key"
db_path = "./meili_data"
env = "development"
max_index_size = "100 GiB"
```

## 🎯 Your First Search

Let's create our first index and perform a search:

### 1. Start Meilisearch

```bash
./meilisearch --master-key="your_master_key"
```

### 2. Create an Index

```bash
curl -X POST 'http://localhost:7700/indexes' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "uid": "movies",
    "primaryKey": "id"
  }'
```

### 3. Add Documents

```bash
curl -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '[
    {
      "id": 1,
      "title": "The Shawshank Redemption",
      "genre": "Drama",
      "year": 1994,
      "rating": 9.3
    },
    {
      "id": 2,
      "title": "The Godfather",
      "genre": "Crime",
      "year": 1972,
      "rating": 9.2
    },
    {
      "id": 3,
      "title": "The Dark Knight",
      "genre": "Action",
      "year": 2008,
      "rating": 9.0
    }
  ]'
```

### 4. Perform Your First Search

```bash
curl 'http://localhost:7700/indexes/movies/search?q=shawshank'
```

**Expected Response:**

```json
{
  "hits": [
    {
      "id": 1,
      "title": "The Shawshank Redemption",
      "genre": "Drama",
      "year": 1994,
      "rating": 9.3,
      "_formatted": {
        "id": 1,
        "title": "<em>The Shawshank Redemption</em>",
        "genre": "Drama",
        "year": 1994,
        "rating": 9.3
      }
    }
  ],
  "query": "shawshank",
  "processingTimeMs": 1,
  "limit": 20,
  "offset": 0,
  "estimatedTotalHits": 1
}
```

## 🔍 Understanding the Response

- **`hits`**: Array of matching documents
- **`query`**: The search query used
- **`processingTimeMs`**: Time taken to process the search (typically < 1ms)
- **`_formatted`**: Highlighted search terms in results
- **`estimatedTotalHits`**: Total number of matches

## 🎮 Interactive Testing

Let's create a simple test script to experiment with Meilisearch:

```bash
#!/bin/bash
# test_meilisearch.sh

MASTER_KEY="your_master_key"
BASE_URL="http://localhost:7700"

# Function to make API calls
api_call() {
  curl -s -H "Authorization: Bearer $MASTER_KEY" "$@"
}

echo "Testing Meilisearch..."

# Create index
echo "Creating movies index..."
api_call -X POST "$BASE_URL/indexes" \
  -H 'Content-Type: application/json' \
  -d '{"uid": "movies", "primaryKey": "id"}'

# Add sample data
echo "Adding movie documents..."
api_call -X POST "$BASE_URL/indexes/movies/documents" \
  -H 'Content-Type: application/json' \
  -d @- << EOF
[
  {"id": 1, "title": "Inception", "director": "Christopher Nolan", "year": 2010},
  {"id": 2, "title": "The Matrix", "director": "Wachowski Sisters", "year": 1999},
  {"id": 3, "title": "Interstellar", "director": "Christopher Nolan", "year": 2014}
]
EOF

# Test search
echo "Searching for 'matrix'..."
api_call "$BASE_URL/indexes/movies/search?q=matrix"

echo "Searching for 'nolan'..."
api_call "$BASE_URL/indexes/movies/search?q=nolan"
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 7700
   lsof -i :7700
   # Kill the process
   kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   # Make binary executable
   chmod +x ./meilisearch
   ```

3. **Master Key Required**
   ```bash
   # Always include master key in API calls
   curl -H "Authorization: Bearer your_master_key" ...
   ```

## 📊 Health Check

Verify Meilisearch is running:

```bash
curl http://localhost:7700/health
```

**Expected Response:**
```json
{"status": "available"}
```

## 🎯 Next Steps

In the next chapter, we'll explore document management - how to add, update, and delete documents in your Meilisearch indexes.

## 📝 Chapter Summary

- ✅ Installed Meilisearch using binary or Docker
- ✅ Configured basic settings and master key
- ✅ Created your first index
- ✅ Added documents and performed searches
- ✅ Understood search response structure
- ✅ Created a test script for experimentation

**Key Takeaways:**
- Meilisearch provides sub-millisecond search responses
- RESTful API makes integration straightforward
- Documents are immediately searchable after indexing
- Master key authentication is required for write operations

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `meilisearch`, `your_master_key`, `movies` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Meilisearch` as an operating subsystem inside **MeiliSearch Tutorial: Lightning Fast Search Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `title`, `year`, `curl` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Meilisearch` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `meilisearch`.
2. **Input normalization**: shape incoming data so `your_master_key` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `movies`.
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
- search upstream code for `meilisearch` and `your_master_key` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Document Management](02-document-management.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
