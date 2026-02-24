---
layout: default
title: "Chapter 5: Vector Stores & Retrieval"
parent: "LangChain Tutorial"
nav_order: 5
---

# Chapter 5: Vector Stores & Retrieval

Welcome to the heart of modern AI applications: **Retrieval-Augmented Generation (RAG)**! Now that you can load and process documents, you need a way to find the most relevant information when answering questions. That's where vector stores and retrieval systems come in.

## What Problem Do Vector Stores Solve?

Imagine you have thousands of documents and want to answer: *"What are the main benefits of our new product?"*

**Traditional Search:**
- Uses keyword matching
- Misses semantic meaning
- Returns exact word matches only

**Vector Search:**
- Understands meaning and context
- Finds conceptually similar content
- Returns relevant information even without exact keywords

## How Vector Search Works

### 1. Text → Numbers (Embeddings)

```python
from langchain_openai import OpenAIEmbeddings

# Create embeddings model
embeddings = OpenAIEmbeddings()

# Convert text to vectors (numbers)
text = "LangChain helps build AI applications"
vector = embeddings.embed_query(text)

print(f"Text: {text}")
print(f"Vector length: {len(vector)}")
print(f"First 5 values: {vector[:5]}")
```

### 2. Storing Vectors

```python
from langchain.vectorstores import FAISS
from langchain.schema import Document

# Create some sample documents
documents = [
    Document(page_content="LangChain is a framework for building AI applications"),
    Document(page_content="FAISS is a library for efficient similarity search"),
    Document(page_content="Embeddings convert text to numerical vectors")
]

# Create vector store
vectorstore = FAISS.from_documents(documents, embeddings)

print(f"Created vector store with {vectorstore.index.ntotal} vectors")
```

### 3. Searching Vectors

```python
# Search for similar content
query = "How do I build AI apps?"
results = vectorstore.similarity_search(query, k=2)

for i, doc in enumerate(results):
    print(f"{i+1}. {doc.page_content}")
```

## How Vector Search Works Under the Hood

Vector search involves several key concepts:

### Embeddings
- **What**: Convert text to high-dimensional vectors
- **Why**: Computers understand numbers better than text
- **How**: Neural networks trained on massive text datasets

### Similarity Search
- **Cosine Similarity**: Measures angle between vectors
- **Euclidean Distance**: Measures straight-line distance
- **Dot Product**: Measures alignment between vectors

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_manual(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Example usage
vec1 = np.array([1, 2, 3])
vec2 = np.array([1, 2, 4])
similarity = cosine_similarity_manual(vec1, vec2)
print(f"Similarity: {similarity}")  # ~0.99 (very similar)
```

## Different Vector Store Options

### 1. FAISS (Facebook AI Similarity Search)

```python
from langchain.vectorstores import FAISS

# Create FAISS vector store
faiss_store = FAISS.from_documents(documents, embeddings)

# Save and load
faiss_store.save_local("faiss_index")
loaded_store = FAISS.load_local("faiss_index", embeddings)
```

### 2. Chroma (Open-source vector database)

```python
from langchain.vectorstores import Chroma

# Create Chroma vector store
chroma_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Chroma automatically persists data
```

### 3. Pinecone (Managed vector database)

```python
from langchain.vectorstores import Pinecone
import pinecone

# Initialize Pinecone
pinecone.init(api_key="your-api-key", environment="your-env")

# Create Pinecone vector store
pinecone_store = Pinecone.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name="langchain-tutorial"
)
```

## Advanced Retrieval Techniques

### 1. Maximum Marginal Relevance (MMR)

```python
# Get diverse results, not just the most similar
results = vectorstore.max_marginal_relevance_search(
    query="AI applications",
    k=5,  # Number of results
    fetch_k=20,  # Number of candidates to consider
    lambda_param=0.5  # Balance between similarity and diversity
)
```

### 2. Similarity Search with Scores

```python
# Get results with similarity scores
results_with_scores = vectorstore.similarity_search_with_score(
    query="machine learning",
    k=3
)

for doc, score in results_with_scores:
    print(f"Score: {score:.3f} - {doc.page_content}")
```

### 3. Filtering by Metadata

```python
# Add metadata to documents
documents_with_metadata = [
    Document(
        page_content="LangChain tutorial for beginners",
        metadata={"difficulty": "beginner", "topic": "framework"}
    ),
    Document(
        page_content="Advanced LangChain patterns",
        metadata={"difficulty": "advanced", "topic": "framework"}
    ),
    Document(
        page_content="FAISS vector search guide",
        metadata={"difficulty": "intermediate", "topic": "vector-search"}
    )
]

# Search with metadata filter
results = vectorstore.similarity_search(
    query="framework tutorial",
    k=2,
    filter={"difficulty": "beginner"}
)
```

## Building a Complete RAG System

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def create_rag_system(documents):
    """Create a complete RAG system"""

    # 1. Create embeddings
    embeddings = OpenAIEmbeddings()

    # 2. Create vector store
    vectorstore = FAISS.from_documents(documents, embeddings)

    # 3. Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}  # Return top 3 results
    )

    # 4. Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",  # Other options: "map_reduce", "refine"
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

# Use the RAG system
documents = [
    Document(page_content="LangChain is a framework for building AI applications with LLMs"),
    Document(page_content="RAG combines retrieval and generation for better answers"),
    Document(page_content="Vector stores enable semantic search of documents")
]

rag_system = create_rag_system(documents)

# Ask questions
result = rag_system.invoke({"query": "What is LangChain?"})
print(result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    print(f"- {doc.page_content}")
```

## How RAG Works Under the Hood

The RAG process has several stages:

### 1. Indexing (Offline)
```
Documents → Text Splitting → Embeddings → Vector Store
```

### 2. Retrieval (Query Time)
```
Query → Embedding → Similarity Search → Relevant Documents
```

### 3. Generation (Query Time)
```
Query + Retrieved Documents → Prompt → LLM → Answer
```

```python
def rag_pipeline_explained(query, documents):
    """Step-by-step explanation of RAG pipeline"""

    print("🔍 RAG Pipeline Steps:")
    print("=" * 50)

    # Step 1: Convert query to embedding
    print("1. Converting query to embedding...")
    query_embedding = embeddings.embed_query(query)
    print(f"   Query vector length: {len(query_embedding)}")

    # Step 2: Find similar documents
    print("2. Finding similar documents...")
    similar_docs = vectorstore.similarity_search_by_vector(query_embedding, k=3)
    print(f"   Found {len(similar_docs)} relevant documents")

    # Step 3: Prepare context
    print("3. Preparing context for LLM...")
    context = "\n\n".join([doc.page_content for doc in similar_docs])

    # Step 4: Generate answer
    print("4. Generating answer with retrieved context...")
    prompt = f"""Use the following context to answer the question:

Context:
{context}

Question: {query}

Answer:"""

    llm = ChatOpenAI()
    response = llm.invoke(prompt)

    print("✅ Answer generated!")
    return response.content
```

## Optimizing Retrieval Performance

### 1. Chunk Size Optimization

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Experiment with different chunk sizes
chunk_sizes = [500, 1000, 1500, 2000]

for size in chunk_sizes:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=int(size * 0.1)  # 10% overlap
    )

    chunks = splitter.split_documents(documents)
    print(f"Chunk size {size}: {len(chunks)} chunks")

    # Test retrieval quality with this chunk size
    # (You would implement quality metrics here)
```

### 2. Embedding Model Selection

```python
# Compare different embedding models
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

models_to_test = [
    OpenAIEmbeddings(model="text-embedding-ada-002"),
    OpenAIEmbeddings(model="text-embedding-3-small"),
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
]

for model in models_to_test:
    print(f"\nTesting {model.__class__.__name__}...")

    # Create vector store with this model
    vectorstore = FAISS.from_documents(documents, model)

    # Test retrieval quality
    results = vectorstore.similarity_search("AI applications", k=3)
    print(f"Retrieved {len(results)} documents")
```

### 3. Hybrid Search

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# Keyword-based retrieval
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 3

# Vector-based retrieval
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Combine both approaches
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]  # Equal weight to both
)

# Use hybrid search
results = ensemble_retriever.get_relevant_documents("AI applications")
```

## Common Vector Store Patterns

### 1. Incremental Updates

```python
# Add new documents without rebuilding
new_documents = [
    Document(page_content="New information about LangChain v0.1.0")
]

vectorstore.add_documents(new_documents)
```

### 2. Metadata Filtering

```python
# Filter by document type, date, author, etc.
results = vectorstore.similarity_search(
    query="machine learning",
    filter={"category": "tutorial", "difficulty": "beginner"}
)
```

### 3. Multi-tenant Applications

```python
# Add tenant information to metadata
documents_with_tenant = [
    Document(
        page_content="Company policy document",
        metadata={"tenant_id": "company_a", "doc_type": "policy"}
    ),
    Document(
        page_content="User guide",
        metadata={"tenant_id": "company_b", "doc_type": "guide"}
    )
]

# Query with tenant filter
company_a_results = vectorstore.similarity_search(
    query="policy information",
    filter={"tenant_id": "company_a"}
)
```

## Troubleshooting Vector Search

### Common Issues and Solutions

```python
# Issue: Poor retrieval quality
# Solution: Experiment with different chunk sizes and overlap
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # Increase overlap
    separators=["\n\n", "\n", " ", ""]  # Better separators
)

# Issue: Slow search
# Solution: Use approximate nearest neighbor search
vectorstore = FAISS.from_documents(
    documents,
    embeddings,
    # FAISS parameters for speed vs accuracy trade-off
)

# Issue: Memory issues with large datasets
# Solution: Use streaming or batch processing
def process_large_dataset(documents, batch_size=100):
    """Process documents in batches to manage memory"""
    all_vectors = []

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_vectors = embeddings.embed_documents(
            [doc.page_content for doc in batch]
        )
        all_vectors.extend(batch_vectors)

    return all_vectors
```

## What We've Learned

Outstanding work! 🎉 You've now mastered:

1. **Vector Embeddings** - Converting text to numerical representations
2. **Vector Stores** - Different storage options (FAISS, Chroma, Pinecone)
3. **Similarity Search** - Finding relevant documents using vector similarity
4. **RAG Systems** - Complete retrieval-augmented generation pipelines
5. **Performance Optimization** - Chunk sizing, model selection, hybrid search
6. **Advanced Patterns** - Metadata filtering, incremental updates, multi-tenancy

## Next Steps

Now that you can retrieve relevant information, let's learn about autonomous agents that can take actions. In [Chapter 6: Agents & Tools](06-agents-tools.md), we'll explore how to build AI systems that can interact with external tools and APIs.

---

**Try this exercise:**
Build a RAG system that can answer questions about a specific domain (like programming, cooking, or history). Experiment with different chunk sizes and embedding models to see what works best for your use case.

*What's the most interesting application you can think of for RAG systems?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `documents`, `print`, `page_content` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Vector Stores & Retrieval` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `vectorstore`, `embeddings`, `vector` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Vector Stores & Retrieval` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `documents`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `page_content`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `documents` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Document Loading & Processing](04-document-processing.md)
- [Next Chapter: Chapter 6: Agents & Tools](06-agents-tools.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
