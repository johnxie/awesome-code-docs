---
layout: default
title: "Chapter 1: Getting Started with LanceDB"
parent: "LanceDB Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with LanceDB

> Install LanceDB, create your first database, and perform basic vector operations.

## Overview

This chapter guides you through installing LanceDB, understanding its architecture, creating databases and tables, and performing your first vector similarity searches.

## Installation

### Python Installation

```bash
# Install LanceDB
pip install lancedb

# Install with optional dependencies
pip install lancedb[embeddings]  # For built-in embedding functions
pip install lancedb[dev]         # For development

# Verify installation
python -c "import lancedb; print(lancedb.__version__)"
```

### JavaScript/TypeScript Installation

```bash
# Using npm
npm install @lancedb/lancedb

# Using yarn
yarn add @lancedb/lancedb

# Using pnpm
pnpm add @lancedb/lancedb

# With vectordb (legacy name)
npm install vectordb
```

### System Requirements

```bash
# Supported platforms
- Linux (x86_64, aarch64)
- macOS (x86_64, ARM64)
- Windows (x86_64)

# Python requirements
- Python 3.8+
- pip 20.0+

# Node.js requirements
- Node.js 18+
```

## Your First Database

### Creating a Database

```python
import lancedb

# Connect to a local database (creates if doesn't exist)
db = lancedb.connect("./my_lancedb")

# Database is stored as files in the directory
# ./my_lancedb/
#   ├── table1.lance/
#   ├── table2.lance/
#   └── ...

print(f"Database location: {db.uri}")
print(f"Tables: {db.table_names()}")
```

### In-Memory Database

```python
import lancedb

# Create an in-memory database (for testing/development)
db = lancedb.connect("memory://")

# Data is not persisted after the process ends
```

### Cloud Storage

```python
import lancedb

# Connect to S3
db = lancedb.connect("s3://my-bucket/my-database")

# Connect to Google Cloud Storage
db = lancedb.connect("gs://my-bucket/my-database")

# Connect to Azure Blob Storage
db = lancedb.connect("az://my-container/my-database")
```

## Creating Tables

### From Python Dictionaries

```python
import lancedb

db = lancedb.connect("./my_lancedb")

# Create table from list of dictionaries
data = [
    {"id": 1, "text": "Hello world", "vector": [0.1, 0.2, 0.3, 0.4]},
    {"id": 2, "text": "Goodbye world", "vector": [0.5, 0.6, 0.7, 0.8]},
    {"id": 3, "text": "LanceDB rocks", "vector": [0.2, 0.3, 0.4, 0.5]},
]

table = db.create_table("my_table", data)

print(f"Table created: {table.name}")
print(f"Row count: {table.count_rows()}")
```

### From Pandas DataFrame

```python
import lancedb
import pandas as pd
import numpy as np

db = lancedb.connect("./my_lancedb")

# Create DataFrame with vector column
df = pd.DataFrame({
    "id": [1, 2, 3],
    "text": ["Hello", "World", "LanceDB"],
    "vector": [
        np.random.rand(384).tolist(),
        np.random.rand(384).tolist(),
        np.random.rand(384).tolist(),
    ]
})

table = db.create_table("pandas_table", df)
```

### From PyArrow

```python
import lancedb
import pyarrow as pa
import numpy as np

db = lancedb.connect("./my_lancedb")

# Create PyArrow table
schema = pa.schema([
    pa.field("id", pa.int64()),
    pa.field("text", pa.string()),
    pa.field("vector", pa.list_(pa.float32(), 384)),
])

data = pa.table({
    "id": [1, 2, 3],
    "text": ["Hello", "World", "LanceDB"],
    "vector": [
        np.random.rand(384).astype(np.float32).tolist(),
        np.random.rand(384).astype(np.float32).tolist(),
        np.random.rand(384).astype(np.float32).tolist(),
    ]
}, schema=schema)

table = db.create_table("arrow_table", data)
```

### With Explicit Schema

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector

# Define schema using Pydantic
class Document(LanceModel):
    id: int
    title: str
    content: str
    vector: Vector(384)  # 384-dimensional vector
    metadata: dict = {}

db = lancedb.connect("./my_lancedb")

# Create table with schema
table = db.create_table("documents", schema=Document)

# Add data
table.add([
    Document(
        id=1,
        title="Introduction",
        content="Welcome to LanceDB",
        vector=[0.1] * 384,
        metadata={"category": "guide"}
    )
])
```

## Basic Vector Search

### Simple Search

```python
import lancedb
import numpy as np

db = lancedb.connect("./my_lancedb")

# Assume table exists with vector column
table = db.open_table("my_table")

# Search by vector
query_vector = np.random.rand(384).tolist()
results = table.search(query_vector).limit(10).to_pandas()

print(results)
# Returns: id, text, vector, _distance (similarity score)
```

### Search with Distance Metric

```python
# Cosine similarity (default)
results = table.search(query_vector) \
    .metric("cosine") \
    .limit(10) \
    .to_pandas()

# L2 (Euclidean) distance
results = table.search(query_vector) \
    .metric("L2") \
    .limit(10) \
    .to_pandas()

# Dot product
results = table.search(query_vector) \
    .metric("dot") \
    .limit(10) \
    .to_pandas()
```

### Filtering Results

```python
# Search with WHERE clause
results = table.search(query_vector) \
    .where("category = 'news'") \
    .limit(10) \
    .to_pandas()

# Multiple conditions
results = table.search(query_vector) \
    .where("category = 'news' AND year >= 2023") \
    .limit(10) \
    .to_pandas()

# IN clause
results = table.search(query_vector) \
    .where("category IN ('news', 'blog', 'article')") \
    .limit(10) \
    .to_pandas()
```

### Selecting Columns

```python
# Select specific columns
results = table.search(query_vector) \
    .select(["id", "title", "content"]) \
    .limit(10) \
    .to_pandas()

# Exclude vector from results (faster)
results = table.search(query_vector) \
    .select(["id", "title"]) \
    .limit(10) \
    .to_pandas()
```

## Adding and Updating Data

### Adding Rows

```python
# Add single row
table.add([{"id": 4, "text": "New document", "vector": [0.1] * 384}])

# Add multiple rows
new_data = [
    {"id": 5, "text": "Document 5", "vector": [0.2] * 384},
    {"id": 6, "text": "Document 6", "vector": [0.3] * 384},
]
table.add(new_data)

# Add from DataFrame
import pandas as pd
df = pd.DataFrame(...)
table.add(df)
```

### Updating Rows

```python
# Update using SQL-like syntax
table.update(
    where="id = 1",
    values={"text": "Updated text"}
)

# Update with dictionary
table.update(
    where="category = 'old'",
    values={"category": "archived", "updated_at": "2024-01-01"}
)
```

### Deleting Rows

```python
# Delete by condition
table.delete("id = 1")

# Delete multiple rows
table.delete("category = 'spam'")

# Delete with complex condition
table.delete("created_at < '2023-01-01' AND status = 'draft'")
```

## JavaScript Usage

### Basic Operations

```javascript
import * as lancedb from '@lancedb/lancedb';

// Connect to database
const db = await lancedb.connect('./my_lancedb');

// Create table
const data = [
    { id: 1, text: 'Hello world', vector: Array(384).fill(0.1) },
    { id: 2, text: 'Goodbye world', vector: Array(384).fill(0.2) },
];

const table = await db.createTable('my_table', data);

// Search
const queryVector = Array(384).fill(0.15);
const results = await table.search(queryVector).limit(10).toArray();

console.log(results);
```

### With TypeScript

```typescript
import * as lancedb from '@lancedb/lancedb';

interface Document {
    id: number;
    text: string;
    vector: number[];
    metadata?: Record<string, unknown>;
}

async function main() {
    const db = await lancedb.connect('./my_lancedb');

    const data: Document[] = [
        { id: 1, text: 'Hello', vector: Array(384).fill(0.1) },
        { id: 2, text: 'World', vector: Array(384).fill(0.2) },
    ];

    const table = await db.createTable<Document>('documents', data);

    const results = await table
        .search(Array(384).fill(0.15))
        .limit(5)
        .toArray();

    results.forEach((doc: Document & { _distance: number }) => {
        console.log(`${doc.text}: ${doc._distance}`);
    });
}

main();
```

## Working with Embeddings

### Using Sentence Transformers

```python
import lancedb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
texts = [
    "The quick brown fox",
    "jumps over the lazy dog",
    "LanceDB is a vector database"
]
embeddings = model.encode(texts)

# Store in LanceDB
db = lancedb.connect("./my_lancedb")

data = [
    {"text": text, "vector": embedding.tolist()}
    for text, embedding in zip(texts, embeddings)
]

table = db.create_table("sentences", data)

# Search
query = "fast animal"
query_embedding = model.encode(query).tolist()
results = table.search(query_embedding).limit(5).to_pandas()
```

### Using OpenAI Embeddings

```python
import lancedb
import openai

client = openai.OpenAI()

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Create table with embeddings
texts = ["Hello world", "Goodbye world", "LanceDB tutorial"]
data = [
    {"text": text, "vector": get_embedding(text)}
    for text in texts
]

db = lancedb.connect("./my_lancedb")
table = db.create_table("openai_embeddings", data)

# Search
query = "greeting"
results = table.search(get_embedding(query)).limit(5).to_pandas()
```

### Built-in Embedding Functions

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

# Get OpenAI embedding function
openai_embed = get_registry().get("openai").create(name="text-embedding-3-small")

# Define model with embedding function
class Document(LanceModel):
    text: str = openai_embed.SourceField()
    vector: Vector(openai_embed.ndims()) = openai_embed.VectorField()

db = lancedb.connect("./my_lancedb")
table = db.create_table("auto_embed", schema=Document)

# Add data - embeddings are created automatically
table.add([
    {"text": "Hello world"},
    {"text": "LanceDB is great"},
])

# Search - query is embedded automatically
results = table.search("greeting").limit(5).to_pandas()
```

## Database Management

### Listing Tables

```python
db = lancedb.connect("./my_lancedb")

# List all tables
tables = db.table_names()
print(f"Tables: {tables}")

# Check if table exists
if "my_table" in db.table_names():
    table = db.open_table("my_table")
```

### Dropping Tables

```python
# Drop a table
db.drop_table("old_table")

# Drop if exists
if "temp_table" in db.table_names():
    db.drop_table("temp_table")
```

### Table Information

```python
table = db.open_table("my_table")

# Get row count
print(f"Rows: {table.count_rows()}")

# Get schema
print(f"Schema: {table.schema}")

# Get table statistics
print(f"Name: {table.name}")
```

## Error Handling

```python
import lancedb
from lancedb.exceptions import LanceDBError

try:
    db = lancedb.connect("./my_lancedb")
    table = db.open_table("nonexistent_table")
except Exception as e:
    print(f"Table not found: {e}")

try:
    # Create table that already exists
    db.create_table("existing_table", data)
except Exception as e:
    print(f"Table already exists: {e}")

# Use create_table with mode
table = db.create_table("my_table", data, mode="overwrite")  # Replace if exists
```

## Best Practices

### Vector Dimensionality

```python
# Always use consistent vector dimensions
EMBEDDING_DIM = 384  # or 768, 1536, etc.

# Validate before inserting
def validate_vector(vector: list) -> bool:
    return len(vector) == EMBEDDING_DIM

# Include dimension in schema
from lancedb.pydantic import LanceModel, Vector

class Document(LanceModel):
    text: str
    vector: Vector(EMBEDDING_DIM)
```

### Batch Operations

```python
# Batch inserts are more efficient
batch_size = 1000
for i in range(0, len(all_data), batch_size):
    batch = all_data[i:i + batch_size]
    table.add(batch)
```

### Connection Management

```python
# Reuse database connections
class DatabaseManager:
    _instance = None
    _db = None

    @classmethod
    def get_db(cls, uri: str = "./my_lancedb"):
        if cls._db is None:
            cls._db = lancedb.connect(uri)
        return cls._db

# Usage
db = DatabaseManager.get_db()
```

## Summary

In this chapter, you've learned:

- **Installation**: Setting up LanceDB for Python and JavaScript
- **Database Creation**: Local, in-memory, and cloud storage options
- **Table Operations**: Creating tables from various data sources
- **Vector Search**: Basic similarity search with filters
- **CRUD Operations**: Adding, updating, and deleting data
- **Embeddings**: Working with different embedding providers
- **Management**: Listing, dropping, and inspecting tables

## Key Takeaways

1. **Serverless**: No server setup required, just connect and use
2. **Flexible Input**: Accept dictionaries, DataFrames, or PyArrow
3. **Built-in Search**: Vector search works out of the box
4. **Filter Support**: SQL-like WHERE clauses for filtering
5. **Embedding Integration**: Easy integration with embedding models

## Next Steps

Now that you have a working LanceDB setup, let's explore Data Modeling in Chapter 2 to learn about schemas, data types, and table design.

---

**Ready for Chapter 2?** [Data Modeling](02-data-modeling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
