---
layout: default
title: "Chapter 2: Data Modeling"
parent: "LanceDB Tutorial"
nav_order: 2
---

# Chapter 2: Data Modeling

Welcome to **Chapter 2: Data Modeling**. In this part of **LanceDB Tutorial: Serverless Vector Database for AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Design effective schemas for vector data, understand Lance data types, and model complex data structures.

## Overview

Proper data modeling is crucial for building efficient vector search applications. This chapter covers schema design, data types, Pydantic models, and best practices for structuring your data in LanceDB.

## Schema Definition

### Using Pydantic Models

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from typing import Optional, List
from datetime import datetime

class Article(LanceModel):
    """Schema for news articles."""
    id: str
    title: str
    content: str
    author: str
    published_at: datetime
    category: str
    tags: List[str]
    vector: Vector(384)  # Embedding dimension
    metadata: Optional[dict] = None

# Create table with schema
db = lancedb.connect("./my_lancedb")
table = db.create_table("articles", schema=Article)

# Add data (validated against schema)
article = Article(
    id="article-001",
    title="Introduction to LanceDB",
    content="LanceDB is a vector database...",
    author="John Doe",
    published_at=datetime.now(),
    category="technology",
    tags=["database", "vectors", "ai"],
    vector=[0.1] * 384
)
table.add([article])
```

### PyArrow Schemas

```python
import pyarrow as pa
import lancedb

# Define schema with PyArrow
schema = pa.schema([
    pa.field("id", pa.string()),
    pa.field("title", pa.string()),
    pa.field("content", pa.string()),
    pa.field("score", pa.float64()),
    pa.field("count", pa.int32()),
    pa.field("is_active", pa.bool_()),
    pa.field("created_at", pa.timestamp("us")),
    pa.field("tags", pa.list_(pa.string())),
    pa.field("vector", pa.list_(pa.float32(), 384)),
    pa.field("metadata", pa.struct([
        pa.field("source", pa.string()),
        pa.field("version", pa.int32())
    ]))
])

db = lancedb.connect("./my_lancedb")
table = db.create_table("pyarrow_table", schema=schema)
```

## Data Types

### Scalar Types

```python
from lancedb.pydantic import LanceModel, Vector
from datetime import datetime, date
from typing import Optional

class ScalarExample(LanceModel):
    # Numeric types
    integer_field: int
    float_field: float

    # String type
    string_field: str

    # Boolean type
    bool_field: bool

    # Date/Time types
    datetime_field: datetime
    date_field: date

    # Optional fields
    optional_string: Optional[str] = None
    optional_int: Optional[int] = None

    # Vector field
    vector: Vector(384)
```

### Collection Types

```python
from lancedb.pydantic import LanceModel, Vector
from typing import List, Dict, Any

class CollectionExample(LanceModel):
    # List of strings
    tags: List[str]

    # List of numbers
    scores: List[float]

    # Nested list
    matrix: List[List[float]]

    # Dictionary (stored as struct)
    metadata: Dict[str, Any]

    # Vector (special list type)
    vector: Vector(384)
```

### Nested Structures

```python
from lancedb.pydantic import LanceModel, Vector
from typing import List, Optional
from pydantic import BaseModel

# Nested model (not LanceModel)
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None
    address: Optional[Address] = None

# Main model with nested structures
class Customer(LanceModel):
    id: str
    name: str
    contact: ContactInfo
    purchase_history: List[str]
    vector: Vector(384)

# Usage
db = lancedb.connect("./my_lancedb")
table = db.create_table("customers", schema=Customer)

customer = Customer(
    id="cust-001",
    name="Alice Smith",
    contact=ContactInfo(
        email="alice@example.com",
        phone="+1234567890",
        address=Address(
            street="123 Main St",
            city="San Francisco",
            country="USA",
            postal_code="94102"
        )
    ),
    purchase_history=["order-001", "order-002"],
    vector=[0.1] * 384
)
table.add([customer])
```

## Vector Fields

### Vector Dimensions

```python
from lancedb.pydantic import LanceModel, Vector

# Common embedding dimensions
class SmallEmbedding(LanceModel):
    text: str
    vector: Vector(384)  # all-MiniLM-L6-v2

class MediumEmbedding(LanceModel):
    text: str
    vector: Vector(768)  # BERT-base, all-mpnet-base-v2

class LargeEmbedding(LanceModel):
    text: str
    vector: Vector(1536)  # OpenAI text-embedding-3-small

class XLargeEmbedding(LanceModel):
    text: str
    vector: Vector(3072)  # OpenAI text-embedding-3-large
```

### Multiple Vector Fields

```python
from lancedb.pydantic import LanceModel, Vector

class MultiVectorDocument(LanceModel):
    """Document with multiple embedding types."""
    id: str
    title: str
    content: str

    # Different embeddings for different purposes
    title_vector: Vector(384)   # Title embedding
    content_vector: Vector(768)  # Content embedding
    summary_vector: Vector(384)  # Summary embedding

# Search on specific vector field
db = lancedb.connect("./my_lancedb")
table = db.create_table("multi_vector", schema=MultiVectorDocument)

# Search by title
results = table.search(query_vector, vector_column_name="title_vector").limit(10).to_pandas()

# Search by content
results = table.search(query_vector, vector_column_name="content_vector").limit(10).to_pandas()
```

## Embedding Functions

### Built-in Embedding Functions

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

# OpenAI embeddings
openai_embed = get_registry().get("openai").create(
    name="text-embedding-3-small"
)

class OpenAIDocument(LanceModel):
    text: str = openai_embed.SourceField()
    vector: Vector(openai_embed.ndims()) = openai_embed.VectorField()

# Sentence Transformers
st_embed = get_registry().get("sentence-transformers").create(
    name="all-MiniLM-L6-v2"
)

class STDocument(LanceModel):
    text: str = st_embed.SourceField()
    vector: Vector(st_embed.ndims()) = st_embed.VectorField()

# Usage - embeddings are created automatically
db = lancedb.connect("./my_lancedb")
table = db.create_table("auto_embed", schema=OpenAIDocument)

# Just add text, vector is computed automatically
table.add([
    {"text": "Hello world"},
    {"text": "LanceDB is great"},
])

# Search with text (automatically embedded)
results = table.search("greeting").limit(5).to_pandas()
```

### Custom Embedding Functions

```python
from lancedb.embeddings import EmbeddingFunction, EmbeddingFunctionRegistry
import numpy as np

@EmbeddingFunctionRegistry.register("my-custom-embedder")
class CustomEmbedder(EmbeddingFunction):
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self._ndims = 384

    def ndims(self) -> int:
        return self._ndims

    def compute_source_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Compute embeddings for source texts."""
        # Your embedding logic here
        embeddings = []
        for text in texts:
            # Example: simple hash-based embedding (not for production!)
            vec = np.random.RandomState(hash(text) % 2**32).rand(self._ndims)
            embeddings.append(vec.tolist())
        return embeddings

    def compute_query_embeddings(self, query: str) -> list[float]:
        """Compute embedding for a query."""
        return self.compute_source_embeddings([query])[0]

# Usage
custom_embed = get_registry().get("my-custom-embedder").create()

class CustomDocument(LanceModel):
    text: str = custom_embed.SourceField()
    vector: Vector(custom_embed.ndims()) = custom_embed.VectorField()
```

## Table Design Patterns

### Document Store

```python
from lancedb.pydantic import LanceModel, Vector
from typing import Optional, List
from datetime import datetime

class Document(LanceModel):
    """General document storage pattern."""
    # Identity
    id: str
    source: str  # 'web', 'pdf', 'api', etc.

    # Content
    title: str
    content: str
    summary: Optional[str] = None

    # Metadata
    author: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[str] = []

    # Chunking info (for large documents)
    chunk_index: Optional[int] = None
    total_chunks: Optional[int] = None
    parent_id: Optional[str] = None  # Reference to parent document

    # Embedding
    vector: Vector(384)
```

### Product Catalog

```python
from lancedb.pydantic import LanceModel, Vector
from typing import Optional, List
from decimal import Decimal

class Product(LanceModel):
    """E-commerce product catalog pattern."""
    # Identity
    sku: str
    name: str

    # Description (for vector search)
    description: str
    features: List[str]

    # Categorization
    category: str
    subcategory: Optional[str] = None
    brand: str

    # Pricing
    price: float
    currency: str = "USD"

    # Inventory
    in_stock: bool
    quantity: int

    # Media
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    # Search vectors
    text_vector: Vector(384)  # Text description embedding
    image_vector: Optional[Vector(512)] = None  # Image embedding
```

### Chat History

```python
from lancedb.pydantic import LanceModel, Vector
from typing import Optional, List
from datetime import datetime

class ChatMessage(LanceModel):
    """Chat conversation storage pattern."""
    # Identity
    message_id: str
    conversation_id: str
    user_id: str

    # Message content
    role: str  # 'user', 'assistant', 'system'
    content: str

    # Timing
    timestamp: datetime

    # Context
    parent_message_id: Optional[str] = None
    metadata: Optional[dict] = None

    # For semantic search over chat history
    vector: Vector(384)

# Example: Find relevant past conversations
def find_similar_conversations(query: str, user_id: str, table, embed_fn):
    query_vector = embed_fn(query)
    results = table.search(query_vector) \
        .where(f"user_id = '{user_id}'") \
        .limit(10) \
        .to_pandas()
    return results
```

### Multi-Modal Data

```python
from lancedb.pydantic import LanceModel, Vector
from typing import Optional
from datetime import datetime

class MultiModalItem(LanceModel):
    """Multi-modal content (text + image + audio)."""
    id: str
    type: str  # 'text', 'image', 'audio', 'video'

    # Content references
    text_content: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    # Metadata
    title: str
    description: Optional[str] = None
    duration_seconds: Optional[float] = None
    file_size_bytes: Optional[int] = None
    mime_type: Optional[str] = None

    # Multiple embedding types
    text_vector: Optional[Vector(384)] = None  # Text embedding
    image_vector: Optional[Vector(512)] = None  # CLIP image embedding
    audio_vector: Optional[Vector(256)] = None  # Audio embedding

    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
```

## Schema Evolution

### Adding Columns

```python
import lancedb
import pyarrow as pa

db = lancedb.connect("./my_lancedb")
table = db.open_table("my_table")

# Add a new column with default value
table.add_columns({
    "new_column": "default_value"
})

# Add computed column
table.add_columns({
    "text_length": "LENGTH(content)"
})
```

### Handling Schema Changes

```python
from lancedb.pydantic import LanceModel, Vector
from typing import Optional

# Original schema
class DocumentV1(LanceModel):
    id: str
    content: str
    vector: Vector(384)

# Updated schema with new fields
class DocumentV2(LanceModel):
    id: str
    content: str
    vector: Vector(384)
    # New fields with defaults
    title: Optional[str] = None
    category: Optional[str] = "uncategorized"
    version: int = 2

# Migration approach
def migrate_table(db, old_name: str, new_name: str):
    old_table = db.open_table(old_name)
    old_data = old_table.to_pandas()

    # Add default values for new columns
    old_data["title"] = None
    old_data["category"] = "uncategorized"
    old_data["version"] = 2

    # Create new table
    new_table = db.create_table(new_name, old_data)
    return new_table
```

## Best Practices

### Naming Conventions

```python
# Table names: lowercase with underscores
table_name = "user_documents"
table_name = "product_catalog"
table_name = "chat_messages"

# Column names: lowercase with underscores
class GoodNaming(LanceModel):
    user_id: str
    created_at: datetime
    is_active: bool
    text_vector: Vector(384)

# Avoid
class BadNaming(LanceModel):
    UserID: str  # Avoid CamelCase
    CreatedAt: datetime
    isActive: bool  # Avoid camelCase
    textVector: Vector(384)
```

### Vector Column Placement

```python
# Put vector column last (better for scanning)
class OptimalLayout(LanceModel):
    id: str
    title: str
    content: str
    category: str
    created_at: datetime
    # Vector last
    vector: Vector(384)
```

### Index-Friendly Filters

```python
# Good: Equality on indexed columns
results = table.search(query_vector) \
    .where("category = 'news'") \
    .limit(10)

# Good: Range queries
results = table.search(query_vector) \
    .where("price >= 10 AND price <= 100") \
    .limit(10)

# Avoid: Complex expressions that can't use indexes
# results = table.search(query_vector) \
#     .where("LOWER(title) LIKE '%search%'") \
#     .limit(10)
```

## Summary

In this chapter, you've learned:

- **Schema Definition**: Using Pydantic and PyArrow schemas
- **Data Types**: Scalar, collection, and nested types
- **Vector Fields**: Dimensions, multiple vectors, and embedding functions
- **Design Patterns**: Document store, product catalog, chat history
- **Schema Evolution**: Adding columns and handling migrations
- **Best Practices**: Naming, layout, and filter optimization

## Key Takeaways

1. **Use Pydantic**: Type-safe schemas with validation
2. **Choose Dimensions Wisely**: Match your embedding model
3. **Multiple Vectors**: Different vectors for different search needs
4. **Auto-Embedding**: Built-in embedding functions simplify development
5. **Plan for Evolution**: Design schemas that can grow

## Next Steps

Now that you understand data modeling, let's explore Vector Operations in Chapter 3 for advanced similarity search techniques.

---

**Ready for Chapter 3?** [Vector Operations](03-vector-operations.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Vector`, `Optional`, `LanceModel` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Data Modeling` as an operating subsystem inside **LanceDB Tutorial: Serverless Vector Database for AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `None`, `lancedb`, `vector` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Data Modeling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Vector`.
2. **Input normalization**: shape incoming data so `Optional` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `LanceModel`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `Vector` and `Optional` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LanceDB](01-getting-started.md)
- [Next Chapter: Chapter 3: Vector Operations](03-vector-operations.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
